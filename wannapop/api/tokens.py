
from .. import db_manager as db
from . import api_bp
from .auth import basic_auth
from flask import current_app
from .auth import token_auth
from ..helper_json import json_request, json_response

@api_bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    current_app.logger.debug(token)
    db.session.commit()
    return json_response({'token': token})

@api_bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    db.session.commit()
    return json_response("Succefully logged out")
