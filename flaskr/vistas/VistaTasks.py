import os
from os import getcwd

import jwt
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug.utils import secure_filename

from modelos import File, Task, TaskSchema, db, FileSchema
from utils.utils import ALLOWED_EXTENSIONS

task_schema = TaskSchema()
file_schema = FileSchema()


class Result:
    def __init__(self, id, original_format, new_format, status, filename):
        self.id = id
        self.original_format = original_format
        self.new_format = new_format
        self.status = status
        self.filename = filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VistaTasks(Resource):

    @jwt_required()
    def get(self):

        # Get user information
        token = request.headers["Authorization"].split(" ")[1]
        decoded_token = jwt.decode(token, "frase-secreta", algorithms=["HS256"])
        user_id = decoded_token["sub"]

        # Get optional parameters
        try:
            max_number_of_results = request.headers['Max']
        except:
            max_number_of_results = -1
        try:
            order = request.headers['Order']
        except:
            order = 0

        # Get data from the database with the needed fields
        results = db.engine.execute(
            """select task.id, task.original_format, task.new_format, task.timestamp, file.filename, task.status
            from username
            left join file on username.id=file.user
            left join task on file.id=task.file
            where 1=1
            and task.original_format is not null
            and username.id = {}""".format(user_id)
        )

        tasks_in_db = [row for row in results]
        tasks = []
        for task in tasks_in_db:
            result = Result(task[0], task[1], task[2], task[5], task[4])
            result_as_dict = result.__dict__
            tasks.append(result_as_dict)

        # List return based on the criteria selected
        result_list = []
        counter = 0
        if order == 0:
            for task in tasks:
                counter += 1
                result_list.append(task)
                if counter == int(max_number_of_results):
                    break
        else:
            for task in tasks[::-1]:
                counter += 1
                result_list.append(task)
                if counter == int(max_number_of_results):
                    break
        return result_list

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
            file_extension = os.path.splitext(sec_filename)[1].split(".")[1]
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

            created_task = task_schema.dump(new_task)
            created_task["confirmation"] = "Task was created successfully"

            return created_task, 201
        else:
            return {'message': 'The file is corrupted or the extension files is not allowed'}, 400
