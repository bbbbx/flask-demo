import os
from PIL import Image
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from albumy.extensions import db
from albumy.settings import Operations

def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = { 'id': user.id, 'operation': operation }
    data.update(**kwargs)
    return s.dump(data)

def validate_token(user, token, opration, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    else:
        return False

    db.session.commit()
    return True

def resize_image(image, filename, base_width):
    '''base_width: int。
    可以是 400 或 800。
    '''
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:  # img.size：图片的宽高，例如 (205, 315)
        return filename + ext
    w_percent = (base_width / float(img.size[0]))
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)  # ANTIALIAS 平滑化

    filename += current_app.config['ALBUMY_PHOTO_SUFFIX'][base_width] + ext
    img.save(
        os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'] ,filename),
        optimize=True,  # 图像是否压缩
        quality=85      # 压缩图像质的质量
    )
    return filename
