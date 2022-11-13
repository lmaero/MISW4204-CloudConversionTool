import os

from flask_mail import Message, Mail
from google.cloud import storage


class MailNotificator(object):
    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)
        self.mail = Mail(self.app)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def send(self, recipient, title, message, resource):
        msg = Message(title, sender='misw4204.grupo09@gmail.com', recipients=[recipient])
        msg.body = message

        storage_client = storage.Client(project="misw4204-grupo9")
        storage_bucket = storage_client.bucket("cloud-conversion-tool-bucket")

        file_to_download_from_bucket = storage_bucket.blob(resource)
        file_to_download_from_bucket.download_to_filename(resource)

        with self.app.open_resource(resource) as fp:
            msg.attach(resource, "audio/{}".format(os.path.splitext(resource)[1]), fp.read())

        self.mail.send(msg)
        return True
