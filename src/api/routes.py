# src/api/routes.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from services.data_ingestion_service import DataIngestionService
from flasgger import swag_from
from api.models import (Usuario, Producao, Processamento, Comercializacao, Importacao, Exportacao)
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

    @app.route('/producao', methods=['GET'])
    #@jwt_required
    @swag_from({
        'summary': 'Return Production Data',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def producao():
        ano = request.args.get('ano')
        produto = request.args.get('produto')
        if ano and produto:
            producao = Producao.query.filter_by(dt_ano=ano, ds_produto=produto).all()
        elif ano and not produto:
            producao = Producao.query.filter_by(dt_ano=ano).all()
        elif not ano and produto:
            producao = Producao.query.filter_by(ds_produto=produto).all()
        else:
            return jsonify({"message":"You must provide a year or a product"}), 400
        producao_dict = [prod.as_dict() for prod in producao]
        return jsonify(producao_dict), 200

    @app.route('/comercializacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Return Commercialization Data',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def comercializacao():
        ano = request.args.get('ano')
        produto = request.args.get('produto')
        if ano and produto:
            comercializacao = Comercializacao.query.filter_by(dt_ano=ano, ds_produto=produto).first()
            return jsonify(comercializacao.as_dict()), 200
        elif ano and not produto:
            comercializacao = Comercializacao.query.filter_by(dt_ano=ano).all()
        elif not ano and produto:
            comercializacao = Comercializacao.query.filter_by(ds_produto=produto).all()
        else:
            return jsonify({"message": "You must provide a year or a product"}), 400
        comercializacao_dict = [prod.as_dict() for prod in comercializacao]
        return jsonify(comercializacao_dict), 200

    @app.route('/exportacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Return Exportation Data',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def exportacao():
        ano = request.args.get('ano')
        pais = request.args.get('pais')
        tipo_prod = request.args.get('tipo')
        query = Exportacao.query
        # adiciona filtros nas consultas
        if ano:
            query = query.filter_by(dt_ano=ano)
        if pais:
            query = query.filter_by(ds_pais=pais)
        if tipo_prod:
            query = query.filter_by(id_tipo_prod_imp_exp=tipo_prod)

        # roda a consulta se tiver pelo menos um filtro ou retorna um erro
        if not ano and not pais and not tipo_prod:
            return jsonify({"message": "You must provide a year or a product"}), 400
        else:
            exportacao = query.all()

        exportacao_dict = [export.as_dict() for export in exportacao]
        return jsonify(exportacao_dict), 200

    @app.route('/importacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Return Importation Data',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def importacao():
        ano = request.args.get('ano')
        pais = request.args.get('pais')
        tipo_prod = request.args.get('tipo')
        query = Importacao.query

        # adiciona filtros nas consultas
        if ano:
            query = query.filter_by(dt_ano=ano)
        if pais:
            query = query.filter_by(ds_pais=pais)
        if tipo_prod:
            query = query.filter_by(id_tipo_prod_imp_exp=tipo_prod)

        # roda a consulta se tiver pelo menos um filtro ou retorna um erro
        if not ano and not pais and not tipo_prod:
            return jsonify({"message": "You must provide a year or a product"}), 400
        else:
            importacao = query.all()

        importacao_dict = [imp.as_dict() for imp in importacao]
        return jsonify(importacao_dict), 200