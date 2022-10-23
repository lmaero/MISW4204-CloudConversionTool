from os import getcwd

import requests
from celery import Celery
from pydub import AudioSegment

from modelos import db, Username

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(task, file):
    file_to_process = getcwd() + "/files/" + file.filename + "." + file.extension
    file_to_export = getcwd() + "/files/" + file.filename + "." + task.new_format

    new_audio = AudioSegment.from_file(file=file_to_process, format=task.original_format)
    new_audio.export(out_f=file_to_export, format=task.new_format)

    user = db.session.query(Username).filter_by(id=file.user).first()

    task.status = "PROCESSED"
    db.session.add(task)
    db.session.commit()

    requests.post("http://mail:7000/api/mail/send",
                  json={"recipient": user.email, "title": "Processed File",
                        "message": "Your file is ready, please find it attached", "resource": file_to_export})
