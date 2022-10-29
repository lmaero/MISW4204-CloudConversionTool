FROM python:3.10.7-slim-buster

WORKDIR /app

COPY . .
RUN ["mkdir","-p","/etc/nginx/conf.d"]
RUN ["mv","./nginx.conf", "/etc/nginx/conf.d/nginx.conf"]

EXPOSE 80

VOLUME /app
VOLUME /app/files

ENV FLASK_DEBUG=1\
    POSTGRES_USER=admin\
    POSTGRES_PASSWORD=admin\
    APP_DB_NAME=postgres\
    MNT_DIR=/mnt/nfs/filestore\
    FILESTORE_IP_ADDRESS=10.59.173.218\
    FILE_SHARE_NAME=vol1

CMD ["sh","-c","./api-init.sh"]
