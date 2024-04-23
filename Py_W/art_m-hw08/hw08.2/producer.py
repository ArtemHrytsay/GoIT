
from bson import json_util


import pika
import config.models
from seed import seed

COUNT_USERS = 100
EXCHANGE_NAME = 'RabbitMQ_HW8'
QUEUE = 'hw8_queue'

def send_data_to_queue():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()
    
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct')
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE)
    
    for i in config.models.User.objects():
        data = i.to_mongo().to_dict()
        channel.basic_publish(exchange=EXCHANGE_NAME, routing_key=QUEUE, body=json_util.dumps(data).encode('utf-8'))
    connection.close()
    return f"До біржі {EXCHANGE_NAME} відправлено {COUNT_USERS} повідомлень"

def seeding_data():
    try:
        seed(COUNT_USERS)
        return True
    except Exception as e:
        print(e)
        return False

def main():

    sd = seeding_data()
    if sd:
        send = send_data_to_queue()
        return send
        
if __name__ == "__main__":
    main()