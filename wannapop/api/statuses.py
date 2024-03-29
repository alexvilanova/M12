from . import api_bp
from .errors import not_found, bad_request
from ..models import Status
from ..helper_json import json_request, json_response
from .auth import token_auth

# Llistar estats disponibles
@api_bp.route('/statuses', methods=['GET'])
@token_auth.login_required
def get_statuses():
    statuses = Status.get_all()

    data = Status.to_dict_collection(statuses)
    return json_response(data)
