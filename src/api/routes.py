# src/api/routes.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from services.data_ingestion_service import DataIngestionService
from flasgger import swag_from
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
    @swag_from({
      'summary': 'Import data from Embrapa',
      'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
      'responses': {
      200: {'description': 'CSV files processed and data saved'},
      401: {'description': 'Unauthorized'},
      500: {'description': 'Error while processing CSV files'}
      }
    })
    @jwt_required()
    def import_csvs_from_embrapa():
        try:
            DataIngestionService.process_multiple_csv()
            return jsonify({"message": "CSV files processed and data saved"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    @swag_from({
      'summary': 'Register a new user',
      'responses': {
      201: {'description': 'user successfully registered and saved in the database'}
      },
      'parameters': [{
      'name': 'body',
      'in': 'body',
      'schema': {
        'type': 'object',
        'properties': {
        'username': {'type': 'string', 'description': 'The username for login', 'example': 'user1'},
        'password': {'type': 'string', 'description': 'The password for login', 'example': 'password1'}
        },
        'required': ['username', 'password']
      }
      }]
    })
    @app.route('/register', methods=['POST'])
    def register():
        username = request.json.get('username')
        password = request.json.get('password')
        hashed_password = generate_password_hash(password)

        #novo_usuario = {"username":username, "password":hashed_password}
        novo_usuario = [{"username": username, "password": hashed_password}]
        PostgresRepository.save_data(Usuario, novo_usuario)

        return jsonify({"message": "User successfully registered and saved in the database"}), 201

    @app.route('/login', methods=['POST'])
    @swag_from({
      'summary': 'Login route',
      'responses': {
      200: {'description': 'login successful and jwt generated'},
      401: {'description': 'Invalid username or password'}
      },
      'parameters': [{
      'name': 'body',
      'in': 'body',
      'schema': {
        'type': 'object',
        'properties': {
        'username': {'type': 'string', 'description': 'The username for login', 'example': 'user1'},
        'password': {'type': 'string', 'description': 'The password for login', 'example': 'password1'}
        },
        'required': ['username', 'password']
      }
      }]
    })
    def login():
      username, password = request.json.get('username'), request.json.get('password')
      user = Usuario.query.filter_by(username=username).first()
      if user and check_password_hash(user.password, password):
        return jsonify(access_token=create_access_token(identity=username)), 200
      return jsonify({"error": "Invalid username or password"}), 401

    @app.route('/protected')
    @jwt_required()
    @swag_from({
        'summary': 'Protected route, accessible only with a valid JWT token.',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Success'},
            401: {'description': 'Unauthorized'}
        }
    })
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200