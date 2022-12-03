from flask import send_file, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from google.cloud import storage

from modelos import File, FileSchema

file_schema = FileSchema()


class VistaFile(Resource):

    @jwt_required()
    def get(self, filename):
        file_to_download = request.form["file_to_download"]

        try:
            file_query = File.query.filter_by(filename=filename).first()
            file = file_schema.dump(file_query)

            original_file_name = file["filename"] + "." + file["task"][0]["original_format"]
            processed_file_name = file["filename"] + "." + file["task"][0]["new_format"]

            storage_client = storage.Client(project="misw4204-grupo9-docker")
            storage_bucket = storage_client.bucket("cloud-conversion-tool-bucket-docker")

            if file:
                if file_to_download == "original":
                    file_to_download_from_bucket = storage_bucket.blob(original_file_name)
                    file_to_download_from_bucket.download_to_filename(original_file_name)

                    return send_file(original_file_name, as_attachment=True)
                if file_to_download == "processed":
                    file_to_download_from_bucket = storage_bucket.blob(processed_file_name)
                    file_to_download_from_bucket.download_to_filename(processed_file_name)

                    return send_file(processed_file_name, as_attachment=True)
            else:
                return {"message": "There is no filename with this name"}

        except BaseException as error:
            return {"message": error}
