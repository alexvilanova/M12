from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from ..models import Order, ConfirmedOrder
from ..helper_json import json_request, json_response
from flask import current_app
from .auth import token_auth

# Fer una oferta per un producte
@api_bp.route('/orders', methods=['POST'])
@token_auth.login_required
def order_product():
    try:
        data = json_request(['product_id', 'offer'])
        data['buyer_id'] = token_auth.current_user().id
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        order = Order.create(**data)
        current_app.logger.debug(order)
        if not order:
            return forbidden_access("You already have an offer on this product.")

        current_app.logger.debug("Order: {}".format(order.to_dict()))
        return json_response(order.to_dict(), 201)

# Editar l’oferta feta per un producte
@api_bp.route('/orders/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_order(id):
    order = Order.get(id)
    
    if not order:
        return not_found("Order not found")
    if token_auth.current_user().id != order.buyer_id:
        return forbidden_access("You cannot modify an order that is not yours")

    confirmed_order = ConfirmedOrder.get_filtered_by(order_id=id)
    if confirmed_order:
        return forbidden_access("You cannot modify an order that is already confirmed")

    try:
        data = json_request(['offer'], False)
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        order.update(**data)
        current_app.logger.debug("MODIFICADO: {}".format(order.to_dict()))
        return json_response(order.to_dict())

# Anul·lar l’oferta feta per un producte
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_order(id):
    order = Order.get(id)
    if not order:
        return not_found("Order not found")
    if token_auth.current_user().id != order.buyer_id:
        return forbidden_access("No puedes eliminar una orden que no es tuya")

    confirmed_order = ConfirmedOrder.get_filtered_by(order_id=id)
    if confirmed_order:
        return forbidden_access("You cannot delete an order that is not yours")

    order.remove()
    return json_response(order.to_dict())
