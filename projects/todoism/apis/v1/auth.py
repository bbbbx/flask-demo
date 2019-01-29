from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request, g
from todoism.models import User
from todoism.apis.v1.errors import api_abort, invalid_token, token_missing

def generate_token(user):
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])    # 使用 token 中的 id 来查询对应的用户对象
    if user is None:
        return False
    g.current_user = user     # 将用户对象存储在 `g` 上
    return True

def get_token():
    if 'Authorization' in request.headers:
        try:
            token_type, token = request.headers['Authorization'].split(None, 1)   # 'a b c'.split(None, 1) => ['a', 'b c']
        except ValueError:    # Authorization 头部为空或 token 为空
            token_type = token = None
    else:
        token_type = token = None
    
    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()

        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()

        return f(*args, **kwargs)
    return decorated
