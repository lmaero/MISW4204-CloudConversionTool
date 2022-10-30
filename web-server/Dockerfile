FROM python:3-slim

WORKDIR /app
COPY requirements.txt nginx.conf ./

RUN set -e && \
    apt-get update && apt-get install nginx ufw -y && \
    ufw allow 6000 && \
    ufw allow 80 && \
    mv ./nginx.conf /etc/nginx/nginx.conf && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 80

VOLUME /app/files

ENV FLASK_DEBUG=1\
    PORT=6000\
    POSTGRES_USER=postgres\
    POSTGRES_PASSWORD=postgres\
    POSTGRES_DB_NAME=postgres\
    SQL_INSTANCE=34.136.115.126

CMD service nginx start && \
    exec gunicorn --log-level DEBUG --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120 --preload wsgi:app
