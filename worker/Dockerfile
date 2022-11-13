FROM python:3-slim

WORKDIR /app
COPY requirements.txt ./

RUN set -e && \
    apt-get update && apt-get install -y ffmpeg lsb-release redis ufw nano && \
    ufw allow 8000 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV FLASK_DEBUG=1\
    PORT=8000 \
    PYTHONUNBUFFERED=TRUE \
    DEV_ENV=1 \
    GOOGLE_APPLICATION_CREDENTIALS="/app/application_default_credentials.json"

CMD exec gunicorn --log-level DEBUG --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120 --preload wsgi:app
