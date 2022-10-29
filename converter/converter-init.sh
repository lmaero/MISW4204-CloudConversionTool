#!/bin/bash

apt-get update
apt-get install -y ffmpeg netcat
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
gunicorn --bind 0.0.0.0:8000 --log-level=DEBUG app:app app.py
