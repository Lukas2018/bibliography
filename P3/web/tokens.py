from jwt import encode
import datetime

from config import Config

JWT_SECRET = Config.JWT_SECRET
JWT_SESSION_TIME = 5


def create_bibliography_add_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "bibliography": True,
        "create": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_bibliography_edit_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "bibliography": True,
        "edit": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_bibliography_delete_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "bibliography": True,
        "delete": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_upload_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "file": True,
        "upload": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_download_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "file": True,
        "download": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_delete_file_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
        "file": True,
        "delete": True
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()