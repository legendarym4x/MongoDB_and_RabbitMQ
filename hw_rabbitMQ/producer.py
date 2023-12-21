import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField, ObjectIdField

fake = Faker()

connect(host='mongodb+srv://maxwel842:pass@cluster0.3vbsiux.mongodb.net/web17?retryWrites=true&w=majority')

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_notifications_queue')


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)


def do_task():
    for _ in range(10):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
        )
        contact.save()

        message = {'contact_id': str(contact.id)}
        channel.basic_publish(exchange='', routing_key='email_notifications_queue', body=json.dumps(message))

    print("Contacts and messages sent to the queue.")
    connection.close()


if __name__ == '__main__':
    do_task()
