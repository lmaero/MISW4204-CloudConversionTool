from flask import send_file, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from modelos import File, FileSchema

file_schema = FileSchema()


class VistaFile(Resource):

    @jwt_required()
    def get(self, filename):
        file_to_download = request.form["file_to_download"]

        try:
            file_query = File.query.filter_by(filename=filename).first()
            file = file_schema.dump(file_query)

            original_file = "/app/files/" + file["filename"] + "." + file["task"][0]["original_format"]
            processed_file = "/app/files/" + file["filename"] + "." + file["task"][0]["new_format"]

            if file:
                if file_to_download == "original":
                    return send_file(original_file, as_attachment=True)
                if file_to_download == "processed":
                    return send_file(processed_file, as_attachment=True)
            else:
                return {"message": "There is no filename with this name"}

        except BaseException as error:
            return {"message": error}
