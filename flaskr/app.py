import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from notificator.Mail import MailNotificator
from vistas.VistaFile import VistaFile
from vistas.VistaLogin import VistaLogin, VistaSignUp
from vistas.VistaTask import VistaTask
from vistas.VistaTasks import VistaTasks

app = Flask(__name__)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD")
APP_DB_NAME = os.environ.get("APP_DB_NAME")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
UPLOAD_FOLDER = './files'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://{}:{}@db:5432/{}'.format(POSTGRES_USER, POSTGRES_PASS,
                                                                                      APP_DB_NAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'misw4204grupo9@gmail.com'
app.config['MAIL_PASSWORD'] = 'hbipfeffulmgidkx'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaFile, '/api/files/<filename>')

notificator = MailNotificator(app)

jwt = JWTManager(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    if FLASK_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=False, host='0.0.0.0', port=port)
