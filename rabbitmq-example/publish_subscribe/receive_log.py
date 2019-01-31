import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] 正在等待消息，按下 Ctrl+C 可以退出。')


def callback(ch, method, properties, body):
    print(" [x] 收到 %r" % body)


channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()
