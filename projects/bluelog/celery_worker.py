from bluelog import create_app
from bluelog.extensions import celery

app = create_app()
app.app_context().push()
