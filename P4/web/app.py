import datetime
import json
from functools import wraps

import requests

from flask import Flask, make_response, flash, url_for
from flask import redirect
from flask import render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from werkzeug.wrappers import Response

from config import Config
from forms import BibliographyForm
import tokens

from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['WTF_CSRF_SECRET_KEY'] = Config.SECRET_KEY
csrf.init_app(app)
session = Config.session
user = Config.user

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=Config.CLIENT_ID,
    client_secret=Config.CLIENT_SECRET,
    api_base_url=Config.API_BASE_URL,
    access_token_url=Config.ACCESS_TOKEN_URL,
    authorize_url=Config.AUTHORIZE_URL,
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        session_id = request.cookies.get('session_id')
        if session.get_username_by_session(session_id) is None:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')
    return render_template('login.html')


@app.route('/callback')
def callback_calling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    user_info = resp.json()
    session_id = session.begin_session(user_info['name'])
    response = make_response(redirect('/index'))
    expire = session.get_session_expire_date(session_id)
    format = '%Y-%m-%d %H:%M:%S.%f'
    expire = datetime.datetime.strptime(expire.decode(), format) - datetime.datetime.now()
    response.set_cookie('session_id', session_id, httponly=True, max_age=expire)
    return response


@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    session.end_session(session_id)
    response = make_response()
    response.set_cookie('session_id', '', httponly=True, expires=0)
    params = {'returnTo': url_for('login', _external=True), 'client_id': 'Jx6rTiO6OnUT8Abjtuovsokysi4JILtK'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/create_bibliography', methods=['GET', 'POST'])
@requires_auth
def create_bibliography():
    form = BibliographyForm()
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    if form.validate_on_submit():
        response = make_response(redirect('/index'))
        token = tokens.create_bibliography_add_token(username)
        data = {
            'name': form.name.data,
            'author': form.author.data,
            'date': str(form.date.data),
            'token': token
        }
        resp = requests.post('http://cdn:5000/' + username + '/bibliography', json=data)
        if resp.status_code == 200:
            flash(resp.content.decode(), 'success')
        else:
            flash(resp.content.decode(), 'warning')
        return response
    return render_template('create_bibliography.html', username=username, form=form)


@app.route('/edit_bibliography', methods=['POST'])
@requires_auth
def edit_bibliography_form():
    form = BibliographyForm()
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    bibliography['date'] = bibliography['date'][:10]
    bibliography['date'] = str(datetime.datetime.strptime(bibliography['date'], '%Y-%m-%d'))
    bibliography['date'] = bibliography['date'][:10]
    username = session.get_username_by_session(request.cookies.get('session_id'))
    return render_template('edit_bibliography.html', username=username, form=form, bibliography=bibliography)


@app.route('/save_edit_bibliography', methods=['POST'])
@requires_auth
def edit_bibliography():
    form = BibliographyForm()
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    response = make_response(redirect('/index'))
    if form.validate_on_submit():
        session_id = request.cookies.get('session_id')
        username = session.get_username_by_session(session_id)
        token = tokens.create_bibliography_edit_token(username)
        data = {
            'name': form.name.data,
            'author': form.author.data,
            'date': str(form.date.data),
            'token': token
        }
        resp = requests.post('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']), json=data)
        if resp.status_code == 200:
            flash(resp.content.decode(), 'success')
        else:
            flash(resp.content.decode(), 'warning')
    return response


@app.route('/delete_bibliography', methods=['POST'])
@requires_auth
def delete_bibliography():
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    response = make_response(redirect('/index'))
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    token = tokens.create_bibliography_delete_token(username)
    data = {
        'token': token
    }
    resp = requests.delete('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']), json=data)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    return response


@app.route('/bibliography_details', methods=['GET', 'POST'])
@requires_auth
def bibliography_details():
    if request.method == 'GET':
        bibliography = json.loads(request.args['messages'])
    else:
        bibliography = request.form.get('bibliography')
        bibliography = json.loads(bibliography.replace("\'", "\""))
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    resp = requests.get('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']) + '/details')
    files = json.loads(resp.text)
    return render_template('bibliography.html', username=username, files=files, bibliography=bibliography)


@app.route('/upload', methods=['POST'])
@requires_auth
def upload_file():
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    token = tokens.create_upload_token(username)
    params = {
        'token': token
    }
    file = request.files.get('file')
    files = {
        'file': (file.filename, file)
    }
    bibliography = request.form.get('bibliography')
    bibliography = json.loads(bibliography.replace("\'", "\""))
    resp = requests.post('http://cdn:5000/' + username + '/bibliography/' + str(bibliography['id']) + '/file/upload',
                         params=params, files=files)
    if resp.status_code == 200:
        flash(resp.content.decode(), 'success')
    else:
        flash(resp.content.decode(), 'warning')
    messages = json.dumps(bibliography)
    response = make_response(redirect(url_for('bibliography_details', messages=messages)))
    return response


@app.route('/download', methods=['POST'])
@requires_auth
def download_file():
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    token = tokens.create_download_token(username)
    file = request.form.get('file')
    file = json.loads(file.replace("\'", "\""))
    data = {
        'token': token
    }
    resp = requests.get('http://cdn:5000/' + username + '/bibliography/file/' + str(file['id']) + '/download',
                        json=data)
    response = Response(response=resp.content, content_type='application/pdf')
    return response


@app.route('/delete', methods=['POST'])
@requires_auth
def delete_file():
    session_id = request.cookies.get('session_id')
    username = session.get_username_by_session(session_id)
    token = tokens.create_delete_file_token(username)
    file = request.form.get('file')
    file = json.loads(file.replace("\'", "\""))
    data = {
        'token': token
    }
    resp = requests.delete('http://cdn:5000/' + username + '/bibliography/file/' + str(file['id']) + '/delete',
                           json=data)
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
