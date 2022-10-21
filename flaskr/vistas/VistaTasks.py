import json
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import Task, TaskSchema


class VistaTasks(Resource):

    @jwt_required()
    def get(self):
        tasks = []
        try:
            tasks = Task.query.all()
            return [TaskSchema.dump(task) for task in tasks]
        except:
            return {"message": "There is no information for tasks"}

