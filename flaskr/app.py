import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db, Username
from vistas.VistaLogin import VistaLogin
from vistas.VistaTasks import VistaTasks
from vistas.VistaTask import VistaTask

app = Flask(__name__)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD")
APP_DB_NAME = os.environ.get("APP_DB_NAME")

# Docker URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://{}:{}@db:5432/{}'.format(POSTGRES_USER, POSTGRES_PASS,
                                                                                      APP_DB_NAME)

# Local URL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://admin:admin@localhost:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')

jwt = JWTManager(app)

# archivo = File(filename='file', extension='mp3', task=tarea.id)

usuario = Username(username='alonso', email='a.cantu@uniandes.edu.co', password='1234')
'''
tarea = Task(original_format='mp3',
             new_format='mp3',
             status='uploaded',
             timestamp='1234',
             user=usuario.id)
'''

db.session.add(usuario)
db.session.commit()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    app.run(debug=True, host='0.0.0.0', port=port)
