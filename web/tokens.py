from os import getenv
from jwt import decode, encode
import datetime

JWT_SECRET = getenv('JWT_SECRET')
JWT_SESSION_TIME = 5


def create_upload_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_download_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username,
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()


def create_delete_token(username):
    exp = datetime.datetime.now() + datetime.timedelta(minutes=JWT_SESSION_TIME)
    payload = {
        "iss": "web",
        "exp": exp,
        "user": username
    }

    return encode(payload, JWT_SECRET, 'HS256').decode()