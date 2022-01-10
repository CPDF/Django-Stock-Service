import json
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('django-challenge_rabbitmq_django', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    print("Stock data: ", body)
    channel.basic_publish(exchange='', routing_key='stock', body=json.dumps(body), properties=properties)

