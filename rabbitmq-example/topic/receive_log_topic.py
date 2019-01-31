import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(
    exchange='topic_logs',
    exchange_type='topic'
)

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write('Usage: %s [binding_key]...\n' % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs',
        queue=queue_name,
        routing_key=binding_key
    )

print(' [*] 正在等待 %r 消息，按下 Ctrl+C 可以退出。' % binding_keys)

def callback(ch, method, properties, body):
    print(" [x] 收到 %r:%r" % (method.routing_key, body))


channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
