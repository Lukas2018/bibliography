FROM python:3.7-alpine
EXPOSE 5000
WORKDIR /var/www
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]