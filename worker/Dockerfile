FROM python:3-slim

WORKDIR /app
COPY requirements.txt ./

RUN set -e && \
    apt-get update && apt-get install -y ffmpeg netcat lsb-release redis ufw nano nfs-common && \
    ufw allow 8000 && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 8000

VOLUME /app/files

ENV FLASK_DEBUG=1\
    PORT=8000

CMD exec gunicorn --log-level DEBUG --bind 0.0.0.0:$PORT --workers 3 --threads 8 --timeout 120 --preload wsgi:app
