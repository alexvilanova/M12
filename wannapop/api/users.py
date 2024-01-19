from . import api_bp
from .errors import not_found, bad_request
from ..models import User, Product
from ..helper_json import json_request, json_response
from flask import current_app, request

# Llistar usuaris i filtrar pel nom
@api_bp.route('/users', methods=['GET'])
def get_users():
    search = request.args.get('name')
    if search:
        my_filter = User.name.like('%' + search + '%')
        users = User.db_query().filter(my_filter).all()
    else:
        users = User.get_all()

    data = []
    for user in users:
        user_dict = User.to_dict(user)
        # Elimina el password antes de enviarlo
        user_dict.pop('_User__password', None)
        data.append(user_dict)

    return json_response(data)

# Veure el perfil públic d’un/a usuari/a
@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    result = User.get(id)
    current_app.logger.debug(result)
    if result:
        user_dict = User.to_dict(result)
        # Elimina el password antes de enviarlo
        if '_User__password' in user_dict:
            del user_dict['_User__password']

        return json_response(user_dict)
    else:
        return not_found("Usuario no encontrado")

# Llistar els productes d’un/a usuari/a
@api_bp.route('/users/<int:id>/products', methods=['GET'])
def get_user_products(id):
    productos = Product.get_all_filtered_by(seller_id=id)
    data = Product.to_dict_collection(productos)

    return json_response(data)
