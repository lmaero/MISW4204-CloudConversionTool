from os import getcwd

from celery import Celery
from pydub import AudioSegment

from modelos import db

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(task, file):
    file_to_process = getcwd() + "/files/" + file.filename + "." + file.extension
    file_to_export = getcwd() + "/files/" + file.filename + "." + task.new_format

    new_audio = AudioSegment.from_file(file=file_to_process, format=task.original_format)
    new_audio.export(out_f=file_to_export, format=task.new_format)

    task.status = "PROCESSED"
    db.session.add(task)
    db.session.commit()
