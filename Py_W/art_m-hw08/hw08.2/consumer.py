import json, os, sys, time, pika
from datetime import datetime
from config.models import User


QUEUE = 'hw8_queue'

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        print(f" [x] Received {message}")
        time.sleep(0.5)
        print(f" [x] Completed {method.delivery_tag} task")
        mark_result = mark_data(message.get('_id'))
        if mark_result:
            print("Done!")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def mark_data(user_id):
    try:
        user = User.objects(id=user_id.get('$oid'))
        user.update(is_send=True)
        return True
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)