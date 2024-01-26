from . import api_bp
from .errors import not_found, bad_request, forbidden_access
from ..models import Order
from ..helper_json import json_request, json_response
from flask import current_app

# Fer una oferta per un producte
@api_bp.route('/orders', methods=['POST'])
def order_product():
    try:
        data = json_request(['product_id', 'buyer_id', 'offer'])
    except Exception as e:
        current_app.logger.debug(e)
        return bad_request(str(e))
    else:
        order = Order.create(**data)
        current_app.logger.debug(order)
        if not order:
            return forbidden_access("Ya has ofertado por este producto")

        current_app.logger.debug("Order: {}".format(order.to_dict()))
        return json_response(order.to_dict(), 201)

# Editar l’oferta feta per un producte
@api_bp.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.get(id)
    if order:
        try:
            data = json_request(['offer'], False)
        except Exception as e:
            current_app.logger.debug(e)
            return bad_request(str(e))
        else:
            order.update(**data)
            current_app.logger.debug("MODIFICADO: {}".format(order.to_dict()))
            return json_response(order.to_dict())
    else:
        return not_found("No se ha encontrado la orden")

# Anul·lar l’oferta feta per un producte
@api_bp.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.get(id)
    if order:
        order.remove()
        return json_response(order.to_dict())
    else:
        return not_found("No se ha encontrado la orden")