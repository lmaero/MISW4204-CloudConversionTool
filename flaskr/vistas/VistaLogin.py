import json

from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from modelos import Username, UsernameSchema, db
from utils.utils import password_check

username_schema = UsernameSchema()


class VistaLogin(Resource):

    def post(self):
        data = json.loads(request.data)
        user = None

        if data:
            if "password" not in data.keys():
                return "You should provide a password", 400
            if "email" not in data.keys() and "username" not in data.keys():
                return "You should provide either an email or an username", 400

            password = data["password"]

            if "username" in data.keys():
                username = data["username"]
                user = Username.query.filter(Username.username == username, Username.password == password).first()
            else:
                email = data["email"]
                user = Username.query.filter(Username.email == email, Username.password == password).first()

        if user is None:
            return "User does not exist", 404
        else:
            token = create_access_token(identity=user.id)
            return {"message": "Successful login", "token": token}


class VistaSignUp(Resource):
    def post(self):
        data = json.loads(request.data)

        try:
            if "password" not in data.keys():
                return "You should provide a password", 400
            if "password_confirmation" not in data.keys():
                return "You should provide a confirmation of your password", 400
            if data["password"] != data["password_confirmation"]:
                return "Your password does not match, please verify it", 400
            if not password_check(data["password"])[0]:  # Check if password is valid
                return password_check(data["password"])[1], 400  # Return corresponding validation message
            if "email" not in data.keys() or "username" not in data.keys():
                return "You should provide either an email or an username", 400
            if db.session.query(Username).filter_by(email=data["email"]).first():
                return "User already registered, please use another email", 400
            if db.session.query(Username).filter_by(username=data["username"]).first():
                return "User already registered, please use another username", 400

            new_user = Username(username=data['username'], password=data['password'], email=data['email'])
            db.session.add(new_user)
            db.session.commit()

            created_user = username_schema.dump(new_user)
            created_user["confirmation"] = "User successfully created"
            del created_user["password"]

            return created_user, 201
        except Exception as e:
            return str(e), 500
