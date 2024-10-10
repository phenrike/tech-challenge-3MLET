import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sua_chave_jwt_secreta_aqui')