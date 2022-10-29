from celery import Celery
from pydub import AudioSegment

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(task, file, user):
    file_to_process = "/app/files/" + file["filename"] + "." + file["extension"]
    file_to_export = "/app/files/" + file["filename"] + "." + task["new_format"]

    new_audio = AudioSegment.from_file(file=file_to_process, format=task["original_format"])
    new_audio.export(out_f=file_to_export, format=task["new_format"])

    # requests.post("http://mail:7000/api/mail/send", json={"recipient": user["email"], "title": "Processed File",
    #                                                       "message": "Your file is ready, please find it attached",
    #                                                       "resource": file_to_export})
