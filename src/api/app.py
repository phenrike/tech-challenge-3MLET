import sys
import os
from datetime import timedelta
from flasgger import Swagger

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from infra.db_connection import init_db
from flask_jwt_extended import JWTManager
from api.routes import configure_routes

def create_app():
    app = Flask(__name__)
    app.config['SWAGGER'] = {
        'title': 'Tech Challenge - API de Vitivinicultura',
        'uiversion': 3,
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'JWT Authorization header usando o esquema Bearer. Exemplo: "Authorization: Bearer {token}"'
            }
        }
    }
    swagger = Swagger(app)

    app.config['JWT_SECRET_KEY'] = 'embrapa'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    # Configurar banco de dados
    init_db(app)

    # Configurar rotas
    configure_routes(app)
    
    return app

app = create_app()  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
