import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db, Username, File, Task
from vistas.VistaFile import VistaFile
from vistas.VistaLogin import VistaLogin, VistaSignUp
from vistas.VistaTasks import VistaTasks
from vistas.VistaTask import VistaTask

app = Flask(__name__)

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASS = os.environ.get("POSTGRES_PASSWORD")
APP_DB_NAME = os.environ.get("APP_DB_NAME")
UPLOAD_FOLDER = './files'

# Docker URL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://{}:{}@db:5432/{}'.format(POSTGRES_USER, POSTGRES_PASS,
                                                                                      APP_DB_NAME)

# Local URL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://admin:admin@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

usuario = Username(username='alonso', email='a.cantu@uniandes.edu.co', password='1234')
db.session.add(usuario)
db.session.commit()

archivo = File(filename='file', extension='mp3', location="home", user=usuario.id)
db.session.add(archivo)
db.session.commit()

archivo2 = File(filename='file', extension='mp3', location="home", user=usuario.id)
db.session.add(archivo2)
db.session.commit()

tarea = Task(original_format='mp3',
             new_format='mp3',
             status='uploaded',
             file=archivo.id)
db.session.add(tarea)
db.session.commit()

tarea2 = Task(original_format='aac',
              new_format='mp3',
              status='uploaded',
              file=archivo2.id)
db.session.add(tarea2)
db.session.commit()

cors = CORS(app)

api = Api(app)
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaTasks, '/api/tasks')
api.add_resource(VistaTask, '/api/tasks/<int:id_task>')
api.add_resource(VistaFile, '/api/files/<filename>')

jwt = JWTManager(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    app.run(debug=False, host='0.0.0.0', port=port)
