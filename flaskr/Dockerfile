FROM python:3-alpine

RUN addgroup app && adduser -S -G app app
USER app

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 6000

ENTRYPOINT [ "python" ]
CMD ["app.py"]
