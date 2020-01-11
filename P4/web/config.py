import os

import redis
from dotenv import load_dotenv

from session import Session
from user import User

load_dotenv()


class Config(object):
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET = os.getenv('JWT_SECRET')
    REDIS_NAME = os.getenv('REDIS_NAME')
    redis = redis.Redis(REDIS_NAME)
    session = Session(redis)
    user = User(redis)
