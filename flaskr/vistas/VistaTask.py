from email import message
from flask import request
from modelos import db, Task, TaskSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from datetime import datetime
#from ..tareas import registrar_log

task_schema= TaskSchema()

class VistaTask(Resource):

    def get(self,id_task):
        try: 
            return task_schema.dump(Task.query.get_or_404(id_task))
        
        except:
            return {"Message":"No task found"}

    


    
