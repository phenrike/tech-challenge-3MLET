# src/api/routes.py
from flask import jsonify
from services.data_ingestion_service import DataIngestionService

def configure_routes(app):
    @app.route('/', methods=['GET'])
    def index():
        return "Tech Challenge - API de Vitivinicultura"

    @app.route('/import-csvs-from-embrapa', methods=['GET'])
    def import_csvs_from_embrapa():
        try:
            # Chama o serviço que processa todos os arquivos CSV
            DataIngestionService.process_multiple_csv()
            return jsonify({"message": "CSV files processed and data saved"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500