import os

import requests
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from google.cloud import storage

from modelos import db, Task, TaskSchema, File, Username, FileSchema, UsernameSchema
from utils.utils import ALLOWED_EXTENSIONS
from vistas.VistaTasks import CONVERTER_IP, CONVERTER_PORT

DEV_ENV = os.environ.get("DEV_ENV")

task_schema = TaskSchema()
file_schema = FileSchema()
username_schema = UsernameSchema()


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
            user = db.session.query(Username).filter_by(id=file.user_id).first()

            storage_client = storage.Client(project="misw4204-grupo9-docker")
            storage_bucket = storage_client.bucket("cloud-conversion-tool-bucket-docker")

            processed_file_name = file.filename + "." + task.new_format
            file_from_bucket = storage_bucket.blob(processed_file_name)
            file_from_bucket.download_to_filename(processed_file_name)

            if task.status == "PROCESSED":
                try:
                    file_from_bucket.delete()
                    os.remove(processed_file_name)
                except Exception as error:
                    return {"message": error}

            task.new_format = request.form["desired_format"]
            task.status = "UPLOADED"
            db.session.add(task)
            db.session.commit()

            local_post_url = "http://worker:8000/api/converter"
            external_post_url = "http://{}:{}/api/converter".format(CONVERTER_IP, CONVERTER_PORT)
            post_url = local_post_url if DEV_ENV == 0 else external_post_url
            requests.post(post_url,
                          json={"task": task_schema.dump(task), "user": username_schema.dump(user),
                                "file": file_schema.dump(file)})

            task.status = "PROCESSED"
            db.session.add(task)
            db.session.commit()

            return task_schema.dump(task), 200
        except Exception as error:
            return {"message": error}

    @jwt_required()
    def delete(self, id_task):
        try:
            # Delete the task
            task = db.session.query(Task).filter(Task.id == id_task).first()
            if task.status == "PROCESSED":

                db.session.delete(task)

                # Delete the file associated to the task
                file = db.session.query(File).filter(File.id == id_task).first()
                db.session.delete(file)

                # Delete original and processed files
                original_file_url = file.filename + "." + task.original_format
                processed_file_url = file.filename + "." + task.new_format

                storage_client = storage.Client(project="misw4204-grupo9-docker")
                storage_bucket = storage_client.bucket("cloud-conversion-tool-bucket-docker")

                original_from_bucket = storage_bucket.blob(original_file_url)
                processed_from_bucket = storage_bucket.blob(processed_file_url)

                original_from_bucket.delete()
                processed_from_bucket.delete()

                os.remove(original_file_url)
                os.remove(processed_file_url)

                db.session.commit()
                return {"message": "The task was removed successfully"}
            else:
                return {"message": "The file is still being processed"}
        except:
            return {"message": "The id provided does not exist in the database"}, 200
