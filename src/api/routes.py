# src/api/routes.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from services.data_ingestion_service import DataIngestionService
from flasgger import swag_from
from api.models import (Usuario, Producao, Processamento, Comercializacao, Importacao, Exportacao, TipoUva, TipoImpExp)
from infra.postgres_repository import PostgresRepository
from sqlalchemy import func

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
      'summary': 'Importa os dados do site da Embrapa',
      'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
      'responses': {
      200: {'description': 'Arquivos CSV processados e dados salvos'},
      401: {'description': 'Não autorizado'},
      500: {'description': 'Erro com o processamento dos arquivos CSV'}
      }
    })
    def import_csvs_from_embrapa():
        try:
            DataIngestionService.process_multiple_csv()
            return jsonify({"message": "Arquivos CSV processados e dados salvos"}), 200
        except Exception as e:
            return jsonify({"Erro": str(e)}), 500
        
    @swag_from({
      'summary': 'Registrar um novo usuário',
      'responses': {
      201: {'description': 'Usuário registrado com sucesso no banco de dados'}
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

        return jsonify({"message": "Usuário registrado com sucesso no banco de dados"}), 201

    @app.route('/login', methods=['POST'])
    @swag_from({
      'summary': 'Login route',
      'responses': {
      200: {'description': 'Login efetuado com sucesso e JWT gerado'},
      401: {'description': 'Usuário ou senha inválidos'}
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
      return jsonify({"Erro": "Usuário ou senha inválidos"}), 401

    @app.route('/protected')
    @jwt_required()
    @swag_from({
        'summary': 'Rota protegida, acessível somente com um tokenb JWT válido.',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Sucesso'},
            401: {'description': 'Não autorizado'}
        }
    })
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

    @app.route('/producao', methods=['GET'])
    #@jwt_required
    @swag_from({
        'summary': 'Retorna dados de produção',
        'parameters': [
            {
                'name': 'ano',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Ano de produção'
            },
            {   'name': 'produto',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Produto'
            },
            {   'name': 'tipo_produto',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de produto comercializado'
            }
        ],
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {
                'description': 'Dados retornados com sucesso',
                'examples': {
                    'application/json': [
                        {
                            "ds_produto": "Tinto",
                            "dt_ano": 1970,
                            "id_producao": 1,
                            "qt_producao": 174224052,
                            "tp_produto": "VINHO DE MESA"
                        }
                    ]
                }
            },
            400: {'description': 'Você deve fornecer um ano ou produto'},
            401: {'description': 'Não autorizado'}
        }
    })
    def producao():
        ano = request.args.get('ano')
        produto = request.args.get('produto')
        tipo_produto = request.args.get('tipo_produto')
        query = Producao.query
        if ano:
            query = query.filter_by(dt_ano=ano)
        if produto:
            query = query.filter(func.lower(Producao.ds_produto) == func.lower(produto))
        if tipo_produto:
            query = query.filter(func.lower(Producao.tp_produto) == func.lower(tipo_produto))
        if not ano and not produto and not tipo_produto:
            return jsonify({"message": "Você deve fornecer um ano, produto ou tipo de produto"}), 400
        else:
            producao = query.all()
        producao_dict = [prod.as_dict() for prod in producao]
        return jsonify(producao_dict), 200

    @app.route('/comercializacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Retorno dos dados de comercialização',
        'parameters': [
            {
                'name': 'ano',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Ano de comercialização'
            },
            {   'name': 'produto',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Produto comercializado'
            },
            {   'name': 'tipo_produto',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de produto comercializado'
            }
        ],
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {
                'description': 'Dados retornados com sucesso',
                'examples': {
                    'application/json': [
                        {
                            "ds_produto": "Tinto",
                            "dt_ano": 1970,
                            "id_producao": 1,
                            "qt_producao": 174224052,
                            "tp_produto": "VINHO DE MESA"
                        }
                    ]
                }
            },
            400: {'description': 'Você deve fornecer um ano, produto ou tipo de produto'},
            401: {'description': 'Não autorizado'}
        }
    })
    def comercializacao():
        ano = request.args.get('ano')
        produto = request.args.get('produto')
        tipo_produto = request.args.get('tipo_produto')
        query = Comercializacao.query
        if ano:
            query = query.filter_by(dt_ano=ano)
        if produto:
            query = query.filter(func.lower(Comercializacao.ds_produto) == func.lower(produto))
        if tipo_produto:
            query = query.filter(func.lower(Comercializacao.tp_produto) == func.lower(tipo_produto))
        if not ano and not produto and not tipo_produto:
            return jsonify({"message": "Você deve fornecer um ano, produto ou tipo de produto"}), 400
        else:
            comercializacao = query.all()
        comercializacao_dict = [prod.as_dict() for prod in comercializacao]
        return jsonify(comercializacao_dict), 200

    @app.route('/exportacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Retorna dados de exportação',
        'parameters': [
            {
                'name': 'ano',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Ano de exportação'
            },
            {   'name': 'pais',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'País de exportação'
            },
            {   'name': 'Tipo de produto',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de produto exportado'
            }
        ],
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {
                'description': 'Dados retornados com sucesso',
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'pais': 'Brasil',
                            'ano': '2023',
                            'produto': 'vinho de mesa',
                            'quantidade': 1000,
                            'valor': 5000
                        }
                    ]
                }
            },
            400: {'description': 'Você deve fornecer um ano, país ou tipo de produto'},
            401: {'description': 'Não autorizado'}
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
            subquery = TipoImpExp.query.filter_by(ds_tipo_prod_imp_exp=tipo_prod).subquery()
            query = query.filter_by(id_tipo_prod_imp_exp=subquery.c.id_tipo_prod_imp_exp)

        # roda a consulta se tiver pelo menos um filtro ou retorna um erro
        if not ano and not pais and not tipo_prod:
            return jsonify({"message": "Você deve fornecer um ano, país ou tipo de produto"}), 400
        else:
            exportacao = query.all()

        exportacao_dict = [export.as_dict() for export in exportacao]
        return jsonify(exportacao_dict), 200

    @app.route('/importacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Retorna dados de importação',
        'parameters': [
            {
                'name': 'ano',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Ano de importação'
            },
            {   'name': 'pais',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'País de importação'
            },
            {   'name': 'tipo_prod',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de produto importado'
            }
        ],
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {
                'description': 'Dados retornados com sucesso',
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'pais': 'Brasil',
                            'ano': '2023',
                            'produto': 'vinho de mesa',
                            'quantidade': 1000,
                            'valor': 5000
                        }
                    ]
                }
            },
            400: {'description': 'Você deve fornecer um ano, país ou tipo de produto'},
            401: {'description': 'Não autorizado'}
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
            subquery = TipoImpExp.query.filter_by(ds_tipo_prod_imp_exp=tipo_prod).subquery()
            query = query.filter_by(id_tipo_prod_imp_exp=subquery.c.id_tipo_prod_imp_exp)

        # roda a consulta se tiver pelo menos um filtro ou retorna um erro
        if not ano and not pais and not tipo_prod:
            return jsonify({"message": "Você deve fornecer um ano, país ou tipo de produto"}), 400
        else:
            importacao = query.all()

        importacao_dict = [imp.as_dict() for imp in importacao]
        return jsonify(importacao_dict), 200

    @app.route('/processamento', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Retorno de dados de processamento',
        'parameters': [
            {
                'name': 'ano',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Ano de exportação'
            },
            {   'name': 'tipo_uva',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de uva processada'
            },
            {   'name': 'tipo_cultivo',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Tipo de cultivo processado'
            }
        ],
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {
                'description': 'Dados retornados com sucesso',
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'pais': 'Brasil',
                            'ano': '2023',
                            'produto': 'vinho de mesa',
                            'quantidade': 1000,
                            'valor': 5000
                        }
                    ]
                }
            },
            400: {'description': 'Você deve fornecer um ano, país ou tipo de produto'},
            401: {'description': 'Não autorizado'}
        }
    })
    def processamento():
        ano = request.args.get('ano')
        tipo_uva = request.args.get('tipo_uva')
        tipo_cultivo = request.args.get('tipo_cultivo')
        query = Processamento.query

        # adiciona filtros nas consultas
        if ano:
            query = query.filter_by(dt_ano=ano)
        if tipo_uva:
            subquery = TipoUva.query.filter_by(ds_tipo_uva=tipo_uva).subquery()
            query = query.filter_by(id_tipo_uva=subquery.c.id_tipo_uva)
        if tipo_cultivo:
            query = query.filter_by(ds_cultivo=tipo_cultivo)

        # roda a consulta se tiver pelo menos um filtro ou retorna um erro
        if not ano and not tipo_uva and not tipo_cultivo:
            return jsonify({"message": "Você deve fornecer um ano, tipo de uva ou tipo de cultivo"}), 400
        else:
            processamento = query.all()

        processamento_dict = [proc.as_dict() for proc in processamento]
        return jsonify(processamento_dict), 200

    @app.route('/tipos_processamento', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Return Types of Processing Filters (Grape Types)',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def tipos_processamento():
        tipos_uva = TipoUva.query.all()
        tipos_dict = [tipo.as_dict() for tipo in tipos_uva]
        return jsonify(tipos_dict), 200

    @app.route('/tipos_importacao_exportacao', methods=['GET'])
    # @jwt_required
    @swag_from({
        'summary': 'Return Types of Processing Filters (Grape Types)',
        'security': [{'Bearer': []}],  # Documenta a necessidade de autenticação
        'responses': {
            200: {'description': 'Data returned successfully'},
            401: {'description': 'Unauthorized'}
        }
    })
    def tipos_importacao_exportacao():
        tipos_imp_exp = TipoImpExp.query.all()
        tipos_dict = [tipo.as_dict() for tipo in tipos_imp_exp]
        return jsonify(tipos_dict), 200