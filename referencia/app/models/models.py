from app.extensions import db

class Comercializacao(db.Model):
    __tablename__ = 'comercializacao'
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(100), nullable=False)  # Correspondente a 'control'
    ano = db.Column(db.Integer, nullable=False)          # Nome da coluna do ano (ex: 1970)
    quantidade = db.Column(db.Float, nullable=True)      # Valor do produto no ano específico

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Producao(db.Model):
    __tablename__ = 'producao'
    id = db.Column(db.Integer, primary_key=True)
    produto = db.Column(db.String(100), nullable=False)  # Correspondente a 'control'
    ano = db.Column(db.Integer, nullable=False)          # Nome da coluna do ano (ex: 1970)
    quantidade = db.Column(db.Float, nullable=True)      # Valor do produto no ano específico

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Exportacao(db.Model):
    __tablename__ = 'exportacao'
    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    kilos = db.Column(db.Float, nullable=True)
    valor_dolar = db.Column(db.Float, nullable=True)
    tipo_produto = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Importacao(db.Model):
    __tablename__ = 'importacao'
    id = db.Column(db.Integer, primary_key=True)
    pais = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    kilos = db.Column(db.Float, nullable=True)
    valor_dolar = db.Column(db.Float, nullable=True)
    tipo_produto = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Modelo para usuários
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {'id': self.id, 'username': self.username}