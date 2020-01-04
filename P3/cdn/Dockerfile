FROM python:3.7-alpine
EXPOSE 5000
WORKDIR /var/www
RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev
RUN pip install psycopg2
RUN apk del .build-deps
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]