from infra.db_connection import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

class Producao(db.Model):
    __tablename__ = 'tbl_producao'
    id_producao = db.Column(db.Integer, primary_key=True)
    ds_produto = db.Column(db.String(255), nullable=False)
    tp_produto = db.Column(db.String(50), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_producao = db.Column(db.Float, nullable=False)

    # Método para retornar o objeto como um dicionário
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Processamento(db.Model):
    __tablename__ = 'tbl_processamento'
    id_processamento = db.Column(db.Integer, primary_key=True)
    id_tipo_uva = db.Column(db.Integer, ForeignKey('tbl_tipo_uva.id_tipo_uva'), nullable=True)
    ds_cultivo = db.Column(db.String(100), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_processamento = db.Column(db.Float, nullable=True)

    # Relacionamento para acessar a descrição
    tipo_uva = relationship("TipoUva", backref="processamentos")

    @property
    def descricao_tipo_uva(self):
        return self.tipo_uva.ds_tipo_uva if self.tipo_uva else None

    def as_dict(self):
        # Inclui todas as colunas do banco e a descrição do tipo de produto
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['descricao_tipo_uva'] = self.descricao_tipo_uva
        return data

class TipoUva(db.Model):
    __tablename__ = 'tbl_tipo_uva'

    id_tipo_uva = db.Column(db.Integer, primary_key=True)
    ds_tipo_uva = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Comercializacao(db.Model):
    __tablename__ = 'tbl_comercializacao'
    id_comercializacao = db.Column(db.Integer, primary_key=True)
    ds_produto = db.Column(db.String(255), nullable=False)
    tp_produto = db.Column(db.String(50), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_comercializacao = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Importacao(db.Model):
    __tablename__ = 'tbl_importacao'
    id_importacao = db.Column(db.Integer, primary_key=True)
    id_tipo_prod_imp_exp = db.Column(db.Integer, ForeignKey('tbl_prod_imp_exp.id_tipo_prod_imp_exp'), nullable=False)
    ds_pais = db.Column(db.String(100), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_importacao = db.Column(db.Float, nullable=False)
    vl_importacao = db.Column(db.Float, nullable=False)

    # Relacionamento para acessar a descrição
    tipo_produto = relationship("TipoImpExp", backref="importacoes")

    @property
    def descricao_tipo_produto(self):
        return self.tipo_produto.ds_tipo_prod_imp_exp if self.tipo_produto else None

    def as_dict(self):
        # Inclui todas as colunas do banco e a descrição do tipo de produto
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['descricao_tipo_produto'] = self.descricao_tipo_produto
        return data

class Exportacao(db.Model):
    __tablename__ = 'tbl_exportacao'

    id_exportacao = db.Column(db.Integer, primary_key=True)
    id_tipo_prod_imp_exp = db.Column(db.Integer, ForeignKey('tbl_prod_imp_exp.id_tipo_prod_imp_exp'), nullable=False)
    ds_pais = db.Column(db.String(100), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_exportacao = db.Column(db.Float, nullable=False)
    vl_exportacao = db.Column(db.Float, nullable=False)

    # Relacionamento para acessar a descrição
    tipo_produto = relationship("TipoImpExp", backref="exportacoes")

    @property
    def descricao_tipo_produto(self):
        return self.tipo_produto.ds_tipo_prod_imp_exp if self.tipo_produto else None

    def as_dict(self):
        # Inclui todas as colunas do banco e a descrição do tipo de produto
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data['descricao_tipo_produto'] = self.descricao_tipo_produto
        return data

class Usuario(db.Model):
    __tablename__ = 'tbl_usuario'

    username = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<username: {self.username}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class TipoImpExp(db.Model):
    __tablename__ = 'tbl_prod_imp_exp'

    id_tipo_prod_imp_exp = db.Column(db.Integer, primary_key=True)
    ds_tipo_prod_imp_exp = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}