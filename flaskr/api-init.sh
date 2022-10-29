#!/bin/bash

apt-get update
apt-get install -y tini nfs-common
apt-get clean
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

set -eo pipefail

# Create mount directory for service.
mkdir -p $MNT_DIR

echo "Mounting Cloud Filestore."

echo $FILESTORE_IP_ADDRESS
echo $FILE_SHARE_NAME
echo $MNT_DIR

mount -o nolock $FILESTORE_IP_ADDRESS:/$FILE_SHARE_NAME $MNT_DIR
echo "Mounting completed."

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
gunicorn --bind 0.0.0.0:6000 --log-level=DEBUG app:app app.py

# Exit immediately when one of the background processes terminate.
wait -n
