import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from modelos import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://postgres:postgrespw@db:5432'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://username:password@localhost:5432/misw4204'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api = Api(app)

jwt = JWTManager(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6000))
    app.run(debug=True, host='0.0.0.0', port=port)
