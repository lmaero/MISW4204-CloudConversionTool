from flask import send_file
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from modelos import File, FileSchema

file_schema = FileSchema()


class VistaFile(Resource):

    @jwt_required()
    def get(self, filename):
        try:
            file_query = File.query.filter_by(filename=filename).first()
            file = file_schema.dump(file_query)

            if file:
                return send_file(file["location"], as_attachment=True)
            else:
                return {"message": "There is no filename with this name"}

        except BaseException as error:
            return {"message": error}
