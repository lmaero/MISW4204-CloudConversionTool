import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db
from vistas.VistaFile import VistaFile
from vistas.VistaHealthCheck import VistaHealthCheck
from vistas.VistaLogin import VistaLogin, VistaSignUp
from vistas.VistaTask import VistaTask
from vistas.VistaTasks import VistaTasks

app = Flask(__name__)

FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
DEV_ENV = os.environ.get("DEV_ENV")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB_NAME")
SQL_INSTANCE = os.environ.get("SQL_INSTANCE")

LOCAL_DB_URL = 'postgresql+pg8000://{}:{}@{}/{}'.format(DB_USER, DB_PASS, "db-local", DB_NAME)
EXTERNAL_DB_URL = 'postgresql+pg8000://{}:{}@{}/{}'.format(DB_USER, DB_PASS, SQL_INSTANCE, DB_NAME)

DB_URL = LOCAL_DB_URL if DEV_ENV == 0 else EXTERNAL_DB_URL

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaHealthCheck, '/')
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaFile, '/api/files/<filename>')

jwt = JWTManager(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    if FLASK_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=False, host='0.0.0.0', port=port)
