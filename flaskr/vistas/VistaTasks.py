import os
from os import getcwd
import jwt
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug.utils import secure_filename

from modelos import File, Task, TaskSchema, db

task_schema = TaskSchema()

ALLOWED_EXTENSIONS = {'mp3', 'acc', 'ogg', 'wav', 'wma'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VistaTasks(Resource):

    @jwt_required()
    def get(self):
        tasks = []
        try:
            tasks = Task.query.all()
            return [task_schema.dump(task) for task in tasks]
        except:
            return {"message": "There is no information for tasks"}

    @jwt_required()
    def post(self):
        token = request.headers["Authorization"].split(" ")[1]
        decoded_token = jwt.decode(token, "frase-secreta", algorithms=["HS256"])
        user_id = decoded_token["sub"]

        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'message': 'No file selected for uploading'}, 400

        if file and allowed_file(file.filename):
            sec_filename = secure_filename(file.filename)
            filename = os.path.splitext(sec_filename)[0]
            file_extension = os.path.splitext(sec_filename)[1]
            file_original = getcwd() + "/files/" + sec_filename
            file.save(file_original)

            new_file = File(
                filename=filename,
                extension=file_extension,
                location=file_original,
                user=user_id
            )

            db.session.add(new_file)
            db.session.commit()

            new_task = Task(
                original_format=file_extension,
                new_format=request.form["new_format"],
                status="UPLOADED",
                file=new_file.id
            )

            db.session.add(new_task)
            db.session.commit()

            file.save(getcwd() + file.filename)
            return task_schema.dump(new_task), 201
