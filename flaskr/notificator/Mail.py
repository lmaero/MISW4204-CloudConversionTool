from flask_mail import Message, Mail


class MailNotificator(object):
    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)
        self.mail = Mail(self.app)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def send(self, recipient, title, message):
        msg = Message(title, sender='misw4204grupo9@gmail.com', recipients=[recipient])
        msg.body = message
        self.mail.send(msg)
        return True
