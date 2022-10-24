import os

from flask_mail import Message, Mail


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

        with self.app.open_resource(resource) as fp:
            msg.attach(resource, "audio/{}".format(os.path.splitext(resource)[1]), fp.read())

        self.mail.send(msg)
        return True
