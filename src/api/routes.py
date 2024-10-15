# src/api/routes.py
from flask import jsonify
from infra.db_connection import db
from services.data_ingestion_service import DataIngestionService

def configure_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        """
        Index route
        ---
        responses:
          200:
            description: Welcome message
        """
        return "Tech Challenge - API de Vitivinicultura"

    @app.route('/import-csvs-from-embrapa', methods=['GET'])
    def import_csvs_from_embrapa():
        """
        Importa CSVs da Embrapa
        ---
        responses:
          200:
            description: CSV files processed and data saved
          500:
            description: Error while processing CSV files
        """
        try:
            DataIngestionService.process_multiple_csv()
            return jsonify({"message": "CSV files processed and data saved"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500