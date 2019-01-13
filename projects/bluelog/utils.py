import re
from unidecode import unidecode
from flask import request, redirect, url_for, current_app
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

def allow_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']

def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def slugify(text, delim=u'-'):
    """Gemerates an ASICC-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        result.extend(unidecode(word).lower().split())
    print(result)
    return unidecode(delim.join(result))
