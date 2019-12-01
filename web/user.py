import hashlib


class User(object):
    def __init__(self, redis_connection):
        self.redis = redis_connection

    def add_user(self, username, password):
        if not self.check_user(username):
            hashed = hashlib.sha256(password.encode()).hexdigest()
            self.redis.hset('users', username, hashed)

    def check_user(self, username):
        return self.redis.hexists('users', username)

    def validate_password(self, username, password):
        if self.check_user(username):
            redis_password = self.redis.hget('users', username).decode()
            password = hashlib.sha256(password.encode()).hexdigest()
            if redis_password == password:
                return True
        return False
