FROM python:3-alpine

RUN addgroup app && adduser -S -G app app
USER app

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r flaskr/requirements.txt

EXPOSE 6000

CMD ["flask", "--app", "app.py", "run"]
