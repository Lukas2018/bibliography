import json
from datetime import datetime
from io import BytesIO

from flask import Flask, send_file, Response, jsonify
from flask import make_response
from flask import request
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from jwt import decode, InvalidTokenError

import notifications
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

import bibliography_storage
from models import File, Bibliography

db.drop_all()
db.create_all()

JWT_SECRET = Config.JWT_SECRET


@app.route('/bibliography', methods=['GET'])
def list_user_bibliographies():
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('bibliography') or not payload.get('list'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliographies = bibliography_storage.get_user_bibliographies(payload.get('username'))
    if bibliographies is None:
        return json.dumps("")
    return jsonify([bibliography.to_dict() for bibliography in bibliographies])


@app.route('/bibliography', methods=['POST'])
def create_bibliography():
    res = request.json
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('bibliography') or not payload.get('create'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    username = payload.get('username')
    bibliography = Bibliography()
    bibliography.name = res['name']
    bibliography.author = res['author']
    bibliography.date = datetime.strptime(res['date'], '%Y-%m-%d')
    bibliography.owner = username
    bibliography.publication_date = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                      '%Y-%m-%d %H:%M:%S')
    bibliography_storage.add_bibliography(bibliography)
    message = "Użytkownik " + username + " dodał bibliografię: " + bibliography.name
    notifications.add_notification_to_user(username, message)
    return make_response('Poprawnie dodano bibliografie', 200)


@app.route("/event/<username>")
@cross_origin()
def event(username):
    return Response(notifications.event_stream(username), mimetype="text/event-stream")


@app.route('/bibliography/<id>', methods=['POST'])
def edit_bibliography(bibliography_id):
    res = request.json
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('bibliography') or not payload.get('edit'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliography = Bibliography()
    bibliography.name = res['name']
    bibliography.author = res['author']
    bibliography.date = datetime.strptime(res['date'], '%Y-%m-%d')
    bibliography.owner = payload.get('username')
    bibliography.publication_date = datetime.strptime(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                                                      '%Y-%m-%d %H:%M:%S')
    bibliography_storage.edit_bibliography(int(bibliography_id), bibliography)
    return make_response('Poprawnie edytowano bibliografie', 200)


@app.route('/bibliography/<id>', methods=['DELETE'])
def delete_bibliography(bibliography_id):
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('bibliography') or not payload.get('delete'):
        return make_response('Nieprawidłowa zawartość tokenu', 404)
    bibliography_storage.delete_bibliography(int(bibliography_id))
    return make_response('Poprawnie usunięto bibliografie', 200)


@app.route('/bibliography/<id>', methods=['GET'])
def list_bibliography_files(bibliography_id):
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('file') or not payload.get('list'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    files = bibliography_storage.get_bibliography_files(int(bibliography_id))
    if files is None:
        return json.dumps("")
    return jsonify([file.to_dict() for file in files])


@app.route('/bibliography/<id>/file', methods=['POST'])
def upload(bibliography_id):
    file = request.files['file']
    if file is None:
        return make_response('Nie podano pliku', 401)
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('file') or not payload.get('upload'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    new_file = File(filename=file.filename, data=file.read(), bibliography_id=int(bibliography_id))
    bibliography_storage.upload_file(new_file)
    return make_response('Pomyślnie dodano plik', 200)


@app.route('/bibliography/file/<id>', methods=['GET'])
def download(file_id):
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('file') or not payload.get('download'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    file = bibliography_storage.get_file(int(file_id))
    return send_file(BytesIO(file.data), attachment_filename="plik.pdf", as_attachment=True)


@app.route('/bibliography/file/<id>', methods=['DELETE'])
def delete(bibliography_id):
    token = request.headers.get('Authorization')
    if token is None:
        return make_response('Brak tokenu', 401)
    if not valid(token):
        return make_response('Nieważny token', 401)
    payload = decode(token, JWT_SECRET)
    if not payload.get('file') or not payload.get('delete'):
        return make_response('Nieprawidłowa zawartość tokenu', 401)
    bibliography_storage.delete_file(bibliography_id)
    return make_response('Pomyślnie usunięto plik', 200)


def valid(token):
    try:
        decode(token, JWT_SECRET)
    except InvalidTokenError as e:
        app.logger.error(str(e))
        return False
    return True
