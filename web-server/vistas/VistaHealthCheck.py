from flask_restful import Resource


class VistaHealthCheck(Resource):
    def get(self):
        return "MISW Cloud Conversion Tool - Grupo 9 - App running!"
