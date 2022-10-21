from email import message
from flask import request
from modelos import db, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_jwt_extended import jwt_required
#from ..tareas import registrar_log


task_schema= TaskSchema()

class VistaTask(Resource):

    @jwt_required()
    def get(self,id_task):
        
        try: 
            return task_schema.dump(Task.query.get_or_404(id_task))
        
        except:
            return {"Message":"No task found"}

    @jwt_required()
    def put(self, id_task):
        

        try:
            task=Task.query.get_or_404(id_task)

            if task.status=="PROCESSED" and request.json.get("new_format",task.new_format):
                task.new_format=request.json.get("new_format",task.new_format)
                task.status="UPLOADED"
                #acá se borra el archivo anterior
                db.session.commit()
                return task_schema.dump(task)

            elif task.status=="UPLOADED":

                if request.jason.get("new_format",task.new_format):
                    task.status=request.json.get("status",task.status)
                    db.session.commit()
                    return task_schema.dump(task)
                else:
                    task.new_status="PROCESSED"
                    db.session.commit()
                    return task_schema.dump(task)

            else:
                return {"Message":"Unexpected error"}

        except:

            return {"Message":"No task found"}
        


    


    
