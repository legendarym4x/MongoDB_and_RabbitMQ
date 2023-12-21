import pika
import json
from mongoengine import connect, Document, StringField, BooleanField

connect(host='mongodb+srv://maxwel842:pass@cluster0.3vbsiux.mongodb.net/web17?retryWrites=true&w=majority')

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email_notifications_queue')


class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    email_sent = BooleanField(default=False)


def send_email(contact_id):
    print(f"Email sent to contact with ID {contact_id}")

    contact = Contact.objects(id=contact_id).first()
    if contact:
        contact.email_sent = True
        contact.save()


def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message.get('contact_id')

    send_email(contact_id)


channel.basic_consume(queue='email_notifications_queue', on_message_callback=callback, auto_ack=True)
print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
