# src/infra/db_connection.py
import os
import psycopg2
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy

# Inicializa o objeto SQLAlchemy
db = SQLAlchemy()

# Configuração da string de conexão
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    try:
        db.init_app(app)
    except Exception as e:
        print(f"Error initializing database: {e}")