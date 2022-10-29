FROM python:3.10.7-slim-buster

WORKDIR /app

COPY . .

EXPOSE 8000

VOLUME /app
VOLUME /app/files

ENV FLASK_DEBUG=1\
    PORT=8000\
    MNT_DIR=/mnt/nfs/filestore\
    FILESTORE_IP_ADDRESS=10.59.173.218\
    FILE_SHARE_NAME=vol1

CMD ["sh","-c","./converter-init.sh"]
