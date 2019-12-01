import datetime
import json
import requests

from flask import Flask, make_response, flash
from flask import redirect
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from werkzeug.wrappers import Response

from config import Config
from forms import RegisterForm, LoginForm
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
        #tokens.create_download_token(username)
        #tokens.create_upload_token(username)
        response = requests.get('http://cdn:5000/' + username)
        files = json.loads(response.text)
        return render_template('index.html', username=username, files=files)
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


@app.route('/download', methods=['POST'])
def download():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    username = session.get_username_by_session(session_id)
    download_token = tokens.create_download_token(username)
    file = request.form.get('file')
    params = {
        'token': download_token
    }
    resp = requests.get('http://cdn:5000/' + username + '/' + file, params=params)
    response = Response(response=resp.content, content_type='application/pdf')
    return response


@app.route('/upload', methods=['POST'])
def upload():
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
    resp = requests.post('http://cdn:5000/upload', files=files, params=params)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    response = make_response(redirect('/index'))
    return response


@app.route('/delete', methods=['POST'])
def delete():
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return redirect('/login')
    username = session.get_username_by_session(session_id)
    delete_token = tokens.create_delete_token(username)
    file = request.form.get('file')
    params = {
        'token': delete_token
    }
    resp = requests.delete('http://cdn:5000/delete' + username + '/' + file, params=params)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    response = make_response('/index')
    return response


if __name__ == '__main__':
    app.run()
