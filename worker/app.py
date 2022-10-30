import os

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource

from general_queue import convert_file

app = Flask(__name__)

FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

app_context = app.app_context()
app_context.push()

cors = CORS(app)


class VistaConverter(Resource):

    def post(self):
        data = request.json
        convert_file(task=data["task"], file=data["file"], user=data["user"])
        return data


api = Api(app)

api.add_resource(VistaConverter, "/api/converter")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    if FLASK_DEBUG:
        app.run(debug=True, host='0.0.0.0', port=port)
    else:
        app.run(debug=False, host='0.0.0.0', port=port)
