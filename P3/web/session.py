import datetime
from uuid import uuid4


class Session(object):
    def __init__(self, redis_store):
        self.redis = redis_store

    def begin_session(self, username):
        session_id = str(uuid4())
        expire_date = str(datetime.datetime.now() + datetime.timedelta(minutes=60))
        self.redis.hset(session_id, 'login', username)
        self.redis.hset(session_id, 'expire', expire_date)
        return session_id

    def end_session(self, session_id):
        self.redis.delete(session_id)

    def get_session_expire_date(self, session_id):
        return self.redis.hget(session_id, 'expire')

    def get_username_by_session(self, session_id):
        return self.redis.hget(session_id, 'login').decode()
