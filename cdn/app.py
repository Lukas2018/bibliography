import json
import os

from dotenv import load_dotenv
from jwt import decode, InvalidTokenError
from flask import Flask, send_file
from flask import request
from flask import make_response

app = Flask(__name__)
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')


@app.route('/<user>')
def index(user):
    if os.path.isdir(user):
        r = os.listdir(user)
        return json.dumps(r)
    else:
        return json.dumps("")


@app.route('/<username>/<file>/download')
def download(username, file):
    token = request.headers.get('token') or request.args.get('token')
    if len(file) == 0:
        return make_response('Brak pliku', 404)
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user', username) != username and payload.get('file', file) != file:
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    path = username + '/' + file
    return send_file(path, as_attachment=True)


@app.route('/<username>/upload', methods=['POST'])
def upload(username):
    file = request.files['file']
    token = request.args.get('token')
    if file is None:
        return make_response('Nie podano pliku', 401)
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    if not os.path.isdir(username):
        os.mkdir(username)
    file.save(os.path.join(username, file.filename))
    file.close()
    return make_response('Pomyślnie dodano plik', 200)

	
@app.route('/<username>/<file>/delete', methods=['DELETE'])
def delete(username, file):
    token = request.headers.get('token') or request.args.get('token')
    if len(file) == 0:
        return make_response('Brak pliku', 404)
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user', username) != username and payload.get('file', file) != file:
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    os.unlink(os.path.join(username, file))
    return make_response('Pomyślnie usunięto plik', 200)

def valid(token):
    try:
        decode(token, JWT_SECRET)
    except InvalidTokenError as e:
        app.logger.error(str(e))
        return False
    return True


def redirect(location):
    response = make_response('', 303)
    response.headers["Location"] = location
    return response
