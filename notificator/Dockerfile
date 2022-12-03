FROM python:3-slim

WORKDIR /app
COPY requirements.txt ./

RUN set -e && \
    apt-get update && apt-get install -y ufw nano && \
    ufw allow 7000 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 7000

ENV FLASK_DEBUG=1\
    PYTHONUNBUFFERED=TRUE\
    GOOGLE_APPLICATION_CREDENTIALS="/app/application_default_credentials.json"

ENTRYPOINT exec flask run --host=0.0.0.0 --port=7000
