import os

import requests
from celery import Celery
from pydub import AudioSegment

NOTIFICATOR_PORT = os.environ.get("NOTIFICATOR_PORT")
NOTIFICATOR_IP = os.environ.get("NOTIFICATOR_IP")

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(task, file, user):
    file_to_process = "/app/files/" + file["filename"] + "." + file["extension"]
    file_to_export = "/app/files/" + file["filename"] + "." + task["new_format"]

    try:
        new_audio = AudioSegment.from_file(file=file_to_process, format=task["original_format"])
        new_audio.export(out_f=file_to_export, format=task["new_format"])
    except BaseException as error:
        print(error)

    requests.post("http://{}:{}/api/mail/send".format(NOTIFICATOR_IP, NOTIFICATOR_PORT),
                  json={"recipient": user["email"], "title": "Processed File",
                        "message": "Your file is ready, please find it attached", "resource": file_to_export})
