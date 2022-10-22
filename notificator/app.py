import os

from flask import Flask, request
from flask_restful import Api, Resource

from Mail import MailNotificator

app = Flask(__name__)

FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'misw4204grupo9@gmail.com'
app.config['MAIL_PASSWORD'] = 'hbipfeffulmgidkx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app_context = app.app_context()
app_context.push()

api = Api(app)

notificator = MailNotificator(app)


class VistaMail(Resource):

    def post(self):
        recipient = request.json["recipient"]
        title = request.json["title"]
        message = request.json["message"]
        print(recipient)
        print(title)
        print(message)

        notificator.send(recipient, title, message)


api.add_resource(VistaMail, "/api/mail/send")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7000))
    if FLASK_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=False, host='0.0.0.0', port=port)
