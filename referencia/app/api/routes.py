from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.models import User

api_bp = Blueprint('api', __name__)

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Usuário ou senha inválidos"}), 401

@api_bp.route('/producao', methods=['GET'])
@jwt_required()
def get_producao():
    from app.models.models import Producao
    producao = Producao.query.all()
    result = [item.as_dict() for item in producao]
    return jsonify(result), 200

# Similarmente, crie endpoints para as outras tabelas