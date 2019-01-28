from werkzeug.http import HTTP_STATUS_CODES
from flask import jsonify

def api_abort(code, message, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES(code, '')
    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response   # 或者返回 (response, code) 元组

