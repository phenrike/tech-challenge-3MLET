# src/api/routes.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from services.data_ingestion_service import DataIngestionService
from api.models import (Usuario)
from infra.postgres_repository import PostgresRepository

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

    @app.route('/register', methods=['POST'])
    def register():
        """
        Registra usuario e salva no banco de dados.
        ---
        responses:
            201:
              description: user successfully registered and saved in the database
        """
        username = request.json.get('username')
        password = request.json.get('password')
        hashed_password = generate_password_hash(password)

        #novo_usuario = {"username":username, "password":hashed_password}
        novo_usuario = [{"username": username, "password": hashed_password}]
        PostgresRepository.save_data(Usuario, novo_usuario)

        return jsonify({"message": "User successfully registered and saved in the database"}), 201

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Trata login do usuario e gera um token JWT.
        ---
        responses:
          200:
            description: login successful and jwt generated
        """

        username = request.json.get('username')
        password = request.json.get('password')
        user = Usuario.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200

        return jsonify({"error": "Invalid username or password"}), 401

    @app.route('/protected')
    @jwt_required()
    def protected():
        """Protected route, accessible only with a valid JWT token."""
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200