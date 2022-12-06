FROM python:3-slim

WORKDIR /app
COPY requirements.txt ./

RUN set -e && \
    apt-get update && apt-get install -y ffmpeg lsb-release ufw && \
    ufw allow 8000 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

ENV DEV_ENV=0\
    GOOGLE_APPLICATION_CREDENTIALS="/app/application_default_credentials.json"

ENTRYPOINT exec python3 app.py
