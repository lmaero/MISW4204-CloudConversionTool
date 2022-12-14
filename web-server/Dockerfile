FROM python:3-slim

WORKDIR /app
COPY requirements.txt nginx.conf ./

RUN set -e && \
    apt-get update && apt-get install -y nginx ufw nano && \
    ufw allow 6000 && \
    ufw allow 80 && \
    mv ./nginx.conf /etc/nginx/nginx.conf && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 80

ENV FLASK_DEBUG=1\
    PORT=6000\
    POSTGRES_USER=postgres\
    POSTGRES_PASSWORD=postgres\
    POSTGRES_DB_NAME=postgres\
    SQL_INSTANCE=35.226.86.191\
    DEV_ENV=1\
    CONVERTER_IP="172.217.203.153"\
    CONVERTER_PORT=""\
    PYTHONUNBUFFERED=TRUE\
    GOOGLE_APPLICATION_CREDENTIALS="/app/application_default_credentials.json"

ENTRYPOINT service nginx start && \
    exec gunicorn --log-level DEBUG --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120 --preload wsgi:app
