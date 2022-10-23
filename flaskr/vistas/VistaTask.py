import os
from os import getcwd

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from general_queue.general_queue import convert_file
from modelos import db, Task, TaskSchema, File
from utils.utils import ALLOWED_EXTENSIONS

task_schema = TaskSchema()


class VistaTask(Resource):

    @jwt_required()
    def get(self, id_task):

        try:
            return task_schema.dump(Task.query.get_or_404(id_task))

        except:
            return {"Message": "No task found"}

    @jwt_required()
    def put(self, id_task):
        if "desired_format" not in request.form:
            return {"message": "You should provide the new format"}, 400
        if request.form["desired_format"] not in ALLOWED_EXTENSIONS:
            return {"message": "That's not a valid extension"}, 400

        try:
            task = Task.query.get_or_404(id_task)
            file = db.session.query(File).filter(File.id == task.file).first()
            processed_file_url = getcwd() + "/files/" + file.filename + "." + task.new_format

            if task.status == "PROCESSED":
                try:
                    os.remove(processed_file_url)
                except Exception as error:
                    return {"message": error}

            task.new_format = request.form["desired_format"]
            task.status = "UPLOADED"
            db.session.add(task)
            db.session.commit()

            convert_file(task, file)

            return task_schema.dump(task), 200
        except Exception as error:
            return {"message": error}

    @jwt_required()
    def delete(self, id_task):
        try:
            # Delete the task
            task = db.session.query(Task).filter(Task.id == id_task).first()
            db.session.delete(task)
            db.session.commit()

            # Delete the file associated to the task
            file = db.session.query(File).filter(File.id == id_task).first()
            db.session.delete(file)
            db.session.commit()
            return {"message": "The task was removed successfully"}
        except:
            return {"message": "The id provided does not exist in the database"}, 200
