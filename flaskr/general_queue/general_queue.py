import requests
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')


@celery_app.task()
def convert_file(file):
    requests.post('http://localhost:6000/api/tasks/', file)
