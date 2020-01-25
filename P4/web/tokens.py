from jwt import encode
import datetime

from config import Config

JWT_SECRET = Config.JWT_SECRET
JWT_SESSION_TIME = 5


def create_bibliography_list_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "bibliography": True,
        "list": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_bibliography_add_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "bibliography": True,
        "create": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_bibliography_edit_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "bibliography": True,
        "edit": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_bibliography_delete_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "bibliography": True,
        "delete": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_file_list_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "file": True,
        "list": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_file_upload_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "file": True,
        "upload": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_file_download_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "file": True,
        "download": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_file_delete_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "username": username,
        "file": True,
        "delete": True
    }
    return encode(payload, JWT_SECRET, 'HS256').decode()