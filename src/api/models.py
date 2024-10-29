from infra.db_connection import db

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
    ds_cultivo = db.Column(db.String(255), nullable=False)  
    ds_tipo_uva = db.Column(db.String(100), nullable=False)  
    dt_ano = db.Column(db.Integer, nullable=False) 
    qt_processamento = db.Column(db.Float, nullable=False)  

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
    id_tipo_prod_imp_exp = db.Column(db.Integer, nullable=False)
    ds_pais = db.Column(db.String(100), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_importacao = db.Column(db.Float, nullable=False)
    vl_importacao = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Exportacao(db.Model):
    __tablename__ = 'tbl_exportacao'

    id_exportacao = db.Column(db.Integer, primary_key=True)
    id_tipo_prod_imp_exp = db.Column(db.Integer, nullable=False)
    ds_pais = db.Column(db.String(100), nullable=False)
    dt_ano = db.Column(db.Integer, nullable=False)
    qt_exportacao = db.Column(db.Float, nullable=False)
    vl_exportacao = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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