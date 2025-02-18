import os
import pika


def get_connection():
    user = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')
    password = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
    host = os.getenv('RABBITMQ_DEFAULT_HOST', 'rabbitmq')
    vhost = os.getenv('RABBITMQ_DEFAULT_VHOST', '/')
    credential = pika.PlainCredentials(username=user, password=password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, virtual_host=vhost, credentials=credential))
    return connection
