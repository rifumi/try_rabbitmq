import json
from aio_pika import ExchangeType
from utils.get_connection import get_connection

def start_consuming_target(binding_keys: list[str]):
    connection = get_connection()
    channel = connection.channel() 

    exchange_name = 'topic_animals'
    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.TOPIC)

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    print(f'binding_keys(queue_bind(routing_key=<arg>)): {binding_keys}')
    if not binding_keys:
        raise ValueError("binding_keys must not be None.")

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        decoded_msg = body.decode('utf-8')
        json_data = json.loads(decoded_msg)
        display_msg = json.dumps(json_data, indent=2)
        print(f" from: {method.routing_key}")
        print(f" Receive: {display_msg}")
        print()

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()
