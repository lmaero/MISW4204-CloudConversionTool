from cgi import test
import glob
from os import getcwd
from pickle import EMPTY_DICT
from queue import Empty
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from modelos import File
from pydub  import AudioSegment


from modelos import db, Task, TaskSchema

task_schema = TaskSchema()

mp3_files = glob.glob('./*.mp3')
acc_files = glob.glob('./*.acc')
ogg_files = glob.glob('./*.ogg')
wav_files = glob.glob('./*.wav')
wma_files = glob.glob('./*.wma')

all_files=[mp3_files,acc_files,ogg_files,wav_files,wma_files]


class VistaTask(Resource):

    @jwt_required()
    def get(self, id_task):

        try:
            return task_schema.dump(Task.query.get_or_404(id_task))

        except:
            return {"Message": "No task found"}

    @jwt_required()
    def put(self, id_task):
        
        
        
        
        task = Task.query.get_or_404(id_task)
        file_id=request.form.get("file",task.file)
        print(request.form.get("file",task.file))
        file_query = File.query.filter_by(id=file_id).first()
        
        print(file_query.filename)
        original_file_url= getcwd()+"/files/"+file_query.filename+file_query.extension
        print(request.form.get("new_format",task.new_format))
        cadena=".mp3"
        print(cadena.replace(".",""))


        try:
            if (request.form.get("status", task.status) == "PROCESSED") and ('new_format' in list(request.form.keys()) ):
                task.new_format = request.form.get("new_format", task.new_format)
                task.status = "UPLOADED"
                # acá se borra el archivo anterior
                db.session.commit()
                return task_schema.dump(task)

            elif request.form.get("status", task.status) == "UPLOADED":
                
                if 'new_format' in list(request.form.keys()):         
                      
                            
                    
                    task.new_format = request.form.get("new_format", task.new_format)
                    db.session.commit()
                    return task_schema.dump(task)
                else:
                     
                    task.status = "PROCESSED"
                    original_format= request.form.get("original",task.original_format).replace(".","")
                    new_format=request.form.get("new_format",task.new_format)

                    new_file_url=getcwd()+"/files/"+file_query.filename+"."+new_format
                    print(new_file_url)

                    new_audio=AudioSegment.from_file(original_file_url,format=original_format)
                    new_audio.export(new_file_url,format=new_format)                    
                    

                    db.session.commit()
                    return task_schema.dump(task)

            else:
                
                return task_schema.dump(task)
                

        except:
            return {"Message": "No task found"}

    @jwt_required()
    def delete(self, id_task):
        try:
            task = db.session.query(Task).filter(Task.id == id_task).first()
            db.session.delete(task)
            db.session.commit()
            return {"message": "The task was removed successfully"}
        except:
            return {"message": "The id provided does not exist in the database"}, 200
