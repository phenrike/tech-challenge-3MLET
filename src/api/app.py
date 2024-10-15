import sys
import os
from flasgger import Swagger

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask
from infra.db_connection import init_db 
from routes import configure_routes

def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    
    # Configurar banco de dados
    init_db(app)

    # Configurar rotas
    configure_routes(app)
    
    return app

if __name__ == "__main__":
    app = create_app()
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=8081, debug=True)
