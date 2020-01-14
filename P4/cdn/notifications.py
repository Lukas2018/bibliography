notifications = {}


def event_stream(username):
    if username in notifications:
        while notifications[username]:
            yield 'data: %s\n\n' % notifications[username].pop(0)


def add_notification_to_user(username, message):
    notifications.setdefault(username, []).append(message)
