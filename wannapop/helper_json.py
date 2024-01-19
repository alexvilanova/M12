from flask import request, jsonify, abort, Response
from werkzeug.http import HTTP_STATUS_CODES

def json_request(required_fields=[], all_required=True):
    data = request.get_json()
    required_count = 0
    for field in required_fields:
        if field not in data:
            if all_required:
                error_message = "Required field '{}' missing".format(field)
                raise Exception(error_message)
        else:
            required_count+=1

    if required_count == 0:
        error_message = "Required field(s) missing"
        raise Exception(error_message)
    
    return data

def json_response(data, status_code=200):
    payload = {
        'success': True,
        'data': data
    }
    response = jsonify(payload)
    response.status_code = status_code
    return response

def json_error_response(status_code, message=None):
    payload = {
        'success': False,
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')
    }
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
