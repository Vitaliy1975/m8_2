import pika
from datetime import datetime
import json
from faker import Faker
from models import Contacts
import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='task_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='task_queue')

fake=Faker()

def seed():
    for _ in range(10):
        contacts=Contacts(fullname=fake.name(),email=fake.email())
        contacts.save()


def main():
    contacts=Contacts.objects()
    # for i in contacts:
        # print(i.to_mongo().to_dict())
    for _,contact in enumerate(contacts):
        message = {
            "id": str(contact.id),
            "email":contact.email,
            "date": datetime.now().isoformat()
        }

        channel.basic_publish(
            exchange='task_mock',
            routing_key='task_queue',
            body=json.dumps(message).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(" [x] Sent %r" % message)
    connection.close()
    
    
if __name__ == '__main__':
    seed()
    main()
