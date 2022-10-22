from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from modelos import db, Task, TaskSchema

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

        try:
            task = Task.query.get_or_404(id_task)

            if task.status == "PROCESSED" and request.json.get("new_format", task.new_format):
                task.new_format = request.json.get("new_format", task.new_format)
                task.status = "UPLOADED"
                # acá se borra el archivo anterior
                db.session.commit()
                return task_schema.dump(task)

            elif task.status == "UPLOADED":

                if request.json.get("new_format", task.new_format):
                    task.status = request.json.get("status", task.status)
                    db.session.commit()
                    return task_schema.dump(task)
                else:
                    task.new_status = "PROCESSED"
                    db.session.commit()
                    return task_schema.dump(task)

            else:
                return {"Message": "Unexpected error"}

        except:
            return {"Message": "No task found"}

    @jwt_required()
    def delete(self, id_task):
        try:
            task = db.session.query(Task).filter(Task.id == id_task).first()
            db.session.delete(task)
            db.session.commit()
        except:
            return {"message": "The id provided does not exist in the database"}
