from celery import Celery

BROKER_URL = 'amqp://'
RESULT_BACKEND = 'amqp'
app = Celery('tasks', backend=RESULT_BACKEND, broker=BROKER_URL)

@app.task
def add(x, y):
    return x + y
