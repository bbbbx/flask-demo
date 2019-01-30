import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

def callback(ch, method, properties, body):
    print(" [x] 收到 %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] 完成")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

print(' [*] 正在等待消息，按下 Ctrl+C 可以退出。')
channel.start_consuming()
