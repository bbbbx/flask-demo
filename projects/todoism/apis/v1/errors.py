from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response   # 或者返回 (response, code) 元组

def invalid_token():
    response = api_abort(401, error='invalid_token', error_description='Token 无效或过期。')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response

def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authoenticate'] = 'Bearer'
    return response
