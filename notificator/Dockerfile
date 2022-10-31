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

VOLUME /app/files

ENV FLASK_DEBUG=1\
    NOTIFICATOR_IP=10.128.0.10\
    NOTIFICATOR_PORT=7000

CMD exec flask run --port=7000
