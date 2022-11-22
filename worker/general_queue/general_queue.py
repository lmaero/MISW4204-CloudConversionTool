import os

import requests
from celery import Celery
from google.cloud import storage
from pydub import AudioSegment

NOTIFICATOR_PORT = os.environ.get("NOTIFICATOR_PORT")
NOTIFICATOR_IP = os.environ.get("NOTIFICATOR_IP")
DEV_ENV = os.environ.get("DEV_ENV")

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(task, file, user):
    storage_client = storage.Client(project="misw4204-grupo9-docker")
    storage_bucket = storage_client.bucket("cloud-conversion-tool-bucket-docker")

    file_to_download = storage_bucket.blob(file["location"])
    file_to_download.download_to_filename(file["location"])

    file_to_process = file["filename"] + "." + file["extension"]
    file_to_export = file["filename"] + "." + task["new_format"]

    try:
        new_audio = AudioSegment.from_file(file=file_to_process, format=task["original_format"])
        new_audio.export(out_f=file_to_export, format=task["new_format"])

        file_to_upload = storage_bucket.blob(file_to_export)
        file_to_upload.upload_from_filename(file_to_export)
    except BaseException as error:
        print(error)

    if DEV_ENV == 0:
        return
    else:
        requests.post("http://{}:{}/api/mail/send".format(NOTIFICATOR_IP, NOTIFICATOR_PORT),
                      json={"recipient": user["email"], "title": "Processed File",
                            "message": "Your file is ready, please find it attached", "resource": file_to_export})
