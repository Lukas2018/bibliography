import json
from datetime import datetime
from io import BytesIO

from flask import Flask, send_file
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from jwt import decode, InvalidTokenError

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

import bibliography_storage
from models import File, Bibliography

db.drop_all()
db.create_all()

JWT_SECRET = Config.JWT_SECRET


@app.route('/<username>')
def list_user_bibliographies(username):
    bibliographies = bibliography_storage.get_user_bibliographies(username)
    if bibliographies is None:
        return json.dumps("")
    return json.dumps([bibliography.to_dict() for bibliography in bibliographies])


@app.route('/<username>/bibliography', methods=['POST'])
def create_bibliography(username):
    res = request.json
    token = res['token']
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user') != username or not payload.get('bibliography') or not payload.get('create'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliography = Bibliography()
    bibliography.name = res['name']
    bibliography.author = res['author']
    bibliography.date = datetime.strptime(res['date'], '%Y-%m-%d')
    bibliography.owner = username
    bibliography.publication_date = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                      '%Y-%m-%d %H:%M:%S')
    bibliography_storage.add_bibliography(bibliography)
    return make_response('Poprawnie dodano bibliografie', 200)


@app.route('/<username>/bibliography/<id>', methods=['POST'])
def edit_bibliography(username, id):
    res = request.json
    token = res['token']
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user') != username or not payload.get('bibliography') or not payload.get('edit'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliography = Bibliography()
    bibliography.name = res['name']
    bibliography.author = res['author']
    bibliography.date = datetime.strptime(res['date'], '%Y-%m-%d')
    bibliography.owner = username
    bibliography.publication_date = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                      '%Y-%m-%d %H:%M:%S')
    bibliography_storage.edit_bibliography(int(id), bibliography)
    return make_response('Poprawnie edytowano bibliografie', 200)


@app.route('/<username>/bibliography/<id>', methods=['DELETE'])
def delete_bibliography(username, id):
    token = request.json['token']
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user') != username or not payload.get('bibliography') or not payload.get('delete'):
        return make_response('Nieprawidłowa zawartość tokenu', 404)
    bibliography_storage.delete_bibliography(int(id))
    return make_response('Poprawnie usunięto bibliografie', 200)


@app.route('/<username>/bibliography/<id>/details')
def list_bibliography_files(username, id):
    files = bibliography_storage.get_bibliography_files(int(id))
    if files is None:
        return json.dumps("")
    return json.dumps([file.to_dict() for file in files])


@app.route('/<username>/bibliography/<id>/file/upload', methods=['POST'])
def upload(username, id):
    file = request.files['file']
    if file is None:
        return make_response('Nie podano pliku', 401)
    new_file = File(filename=file.filename, data=file.read(), bibliography_id=int(id))
    bibliography_storage.upload_file(new_file)
    return make_response('Pomyślnie dodano plik', 200)


@app.route('/<username>/bibliography/file/<id>/download', methods=['GET', 'POST'])
def download(username, id):
    token = request.json['token']
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user') != username or not payload.get('file') or not payload.get('download'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    file = bibliography_storage.get_file(int(id))
    return send_file(BytesIO(file.data), attachment_filename="plik.pdf", as_attachment=True)


@app.route('/<username>/bibliography/file/<id>/delete', methods=['DELETE'])
def delete(username, id):
    token = request.json['token']
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if payload.get('user') != username or not payload.get('file') or not payload.get('delete'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliography_storage.delete_file(id)
    return make_response('Pomyślnie usunięto plik', 200)


def valid(token):
    try:
        decode(token, JWT_SECRET)
    except InvalidTokenError as e:
        app.logger.error(str(e))
        return False
    return True
