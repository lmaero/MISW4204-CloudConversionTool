import json
import os

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app import app
from modelos import Task, TaskSchema, db

task_schema = TaskSchema()


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
        file = request.files['file']
        data = json.loads(request.data)
        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400
        if file.filename == '':
            return {'message': 'No file selected for uploading'}, 400
        if file and data:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            new_task = Task(
                original_format=data["original_format"],
                new_format=data["new_format"],
                status="uploaded",
                file=path
            )
            db.session.add(new_task)
            db.session.commit()
            file.save(path)
            return TaskSchema.dump(new_task), 201
        else:
            return {'message': 'File not allowed'}, 400
