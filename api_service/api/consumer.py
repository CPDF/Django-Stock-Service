import json
import pika
import django
from sys import path
from os import environ

from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer

connection = pika.BlockingConnection(pika.ConnectionParameters('django-challenge_rabbitmq_django', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='stock')

def callback(ch, method, properties, body):
    print("Received in likes...")
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'stock_check':
        quote = Quote.objects.create(id=data['id'], title=data['title'])
        quote.save()
        #print("quote created")
channel.basic_consume(queue='likes', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()