import time

notifications = {}


def event_stream(username):
    if username in notifications:
        for msg in notifications[username]:
            time.sleep(4)
            if notifications[username]:
                notifications[username].pop(0)
            yield 'data: %s\n\n' % msg


def add_notification_to_user(username, message):
    notifications.setdefault(username, []).append(message)
