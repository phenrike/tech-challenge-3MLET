# src/infra/db_connection.py
import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    # Obter a URL do banco de dados a partir da variável de ambiente
    database_url = os.getenv('DATABASE_URL')

    # Fazer o parsing da URL do banco de dados
    result = urlparse(database_url)

    # Extrair as informações da URL
    dbname = result.path[1:]  # Remover a barra inicial do nome do banco de dados
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port

    # Criar a conexão com o banco de dados PostgreSQL
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    return conn
