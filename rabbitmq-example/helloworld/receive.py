import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, methods, properties, body):
    print(" [x] 收到 %r" % body)

channel.basic_consume(callback, queue='hello', no_ack=True)

print(' [*] 正在等待消息，按下 Ctrl+C 可以退出。')
channel.start_consuming()
