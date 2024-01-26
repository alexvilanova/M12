from . import api_bp
from ..helper_json import json_error_response
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

def bad_request(message):
    return json_error_response(400, message)

def forbidden_access(message):
    return json_error_response(403, message)

def not_found(message):
    return json_error_response(404, message)

# Catch all HTTP exceptions
# For example: abort(401)
@api_bp.errorhandler(HTTPException)
def handle_exception(e):
    return json_error_response(e.code)

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    return payload, status_code
