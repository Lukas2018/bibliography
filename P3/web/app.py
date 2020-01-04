import datetime
import json
import requests

from flask import Flask, make_response, flash, url_for
from flask import redirect
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from werkzeug.wrappers import Response

from config import Config
from forms import RegisterForm, LoginForm, BibliographyForm
import tokens

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = Config.SECRET_KEY
csrf.init_app(app)
session = Config.session
user = Config.user


@app.route('/')
@app.route('/index')
def index():
    session_id = request.cookies.get('session_id')
    if session_id:
        username = session.get_username_by_session(session_id)
        response = requests.get('http://cdn:5000/' + username)
        bibliographies = json.loads(response.text)
        return render_template('index.html', username=username, bibliographies=bibliographies)
    return redirect("/login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user.add_user(username, password)
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        session_id = session.begin_session(username)
        response = make_response(redirect('/index'))
        expire = session.get_session_expire_date(session_id)
        format = '%Y-%m-%d %H:%M:%S.%f'
        expire = datetime.datetime.strptime(expire.decode(), format) - datetime.datetime.now()
        response.set_cookie('session_id', session_id, httponly=True, max_age=expire)
        return response
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    session.end_session(session_id)
    response = redirect('/login')
    response.set_cookie('session_id', '', httponly=True, expires=0)
    return response


@app.route('/create_bibliography', methods=['GET', 'POST'])
def create_bibliography():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/login")
    form = BibliographyForm()
    if form.validate_on_submit():
        response = make_response(redirect('/index'))
        username = session.get_username_by_session(session_id)
        token = tokens.create_bibliography_add_token(username)
        params = {
            'token': token
        }
        data = {
            'name': form.name.data,
            'author': form.author.data,
            'date': str(form.date.data)
        }
        resp = requests.post('http://cdn:5000/' + username + '/bibliography', json=data, params=params)
        if resp.status_code == 200:
            flash(resp.content.decode(), 'success')
        else:
            flash(resp.content.decode(), 'warning')
        return response
    return render_template('create_bibliography.html', form=form)


@app.route('/edit_bibliography', methods=['POST'])
def edit_bibliography_form():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/login")
    form = BibliographyForm()
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    bibliography['date'] = bibliography['date'][:10]
    bibliography['date'] = str(datetime.datetime.strptime(bibliography['date'], '%Y-%m-%d'))
    bibliography['date'] = bibliography['date'][:10]
    return render_template('edit_bibliography.html', form=form, bibliography=bibliography)


@app.route('/save_edit_bibliography', methods=['POST'])
def edit_bibliography():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/login")
    form = BibliographyForm()
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    response = make_response(redirect('/index'))
    if form.validate_on_submit():
        username = session.get_username_by_session(session_id)
        token = tokens.create_bibliography_edit_token(username)
        params = {
            'token': token
        }
        data = {
            'name': form.name.data,
            'author': form.author.data,
            'date': str(form.date.data)
        }
        resp = requests.post('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']), json=data, params=params)
        if resp.status_code == 200:
            flash(resp.content.decode(), 'success')
        else:
            flash(resp.content.decode(), 'warning')
    return response


@app.route('/delete_bibliography', methods=['POST'])
def delete_bibliography():
    session_id = request.cookies.get('session_id')
    if not session_id:
        return redirect("/login")
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    response = make_response(redirect('/index'))
    username = session.get_username_by_session(session_id)
    token = tokens.create_bibliography_delete_token(username)
    params = {
        'token': token
    }
    resp = requests.delete('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']), params=params)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    return response


@app.route('/bibliography_details', methods=['GET', 'POST'])
def bibliography_details():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    if request.method == 'GET':
        bibliography = json.loads(request.args['messages'])
    else:
        bibliography = request.form.get('bibliography')
        bibliography = json.loads(bibliography.replace("\'", "\""))
    username = session.get_username_by_session(session_id)
    resp = requests.get('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']) + '/details')
    files = json.loads(resp.text)
    return render_template('bibliography.html', files=files, bibliography=bibliography)


@app.route('/upload', methods=['POST'])
def upload_file():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    username = session.get_username_by_session(session_id)
    file = request.files.get('file')
    upload_token = tokens.create_upload_token(username)
    files = {
        'file': (file.filename, file)
    }
    params = {
        'username': username,
        'token': upload_token
    }
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    resp = requests.post('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']) + '/file/upload', files=files, params=params)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    messages = json.dumps(bibliography)
    response = make_response(redirect(url_for('bibliography_details', messages=messages)))
    return response


@app.route('/download', methods=['POST'])
def download_file():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    username = session.get_username_by_session(session_id)
    download_token = tokens.create_download_token(username)
    file = request.form.get('file')
    file = json.loads(file.replace("\'", "\""))
    params = {
        'token': download_token
    }
    resp = requests.get('http://cdn:5000/' + username + '/bibliography/file/' + str(file['id']) + '/download', params=params)
    response = Response(response=resp.content, content_type='application/pdf')
    return response


@app.route('/delete', methods=['POST'])
def delete_file():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    username = session.get_username_by_session(session_id)
    delete_token = tokens.create_delete_file_token(username)
    file = request.form.get('file')
    file = json.loads(file.replace("\'", "\""))
    params = {
        'token': delete_token
    }
    resp = requests.delete('http://cdn:5000/' + username + '/bibliography/file/' + str(file['id']) + '/delete', params=params)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    messages = json.dumps(bibliography)
    response = make_response(redirect(url_for('bibliography_details', messages=messages)))
    return response


if __name__ == '__main__':
    app.run()