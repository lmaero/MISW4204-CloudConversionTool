#!/bin/bash

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
gunicorn --bind 0.0.0.0:6000 --log-level=DEBUG app:app app.py
