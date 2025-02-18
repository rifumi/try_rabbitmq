#!/usr/bin/env python
import json
from aio_pika import ExchangeType

from utils.get_connection import get_connection

def my_publish(binding_keys: list[str]):
    connection = get_connection()
    channel = connection.channel()

    exchange_name = 'topic_animals'
    channel.exchange_declare(exchange=exchange_name, exchange_type=ExchangeType.TOPIC)

    for counter, routing_key in enumerate(binding_keys):
        ''' routing_key: celerity.color.animal'''
        message = {
            "my_desire": [
                "I want some money!",
                "More pizza!",
                ],
            "exchange_name": exchange_name,
            "no.": counter,
            }
        dumped_message = json.dumps(message)
        message_body = dumped_message.encode('utf-8')
        channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=message_body)
        formatted_msg = json.dumps(message, indent=2)
        print(f' To: {routing_key}')
        print(f' Sent: {formatted_msg}' '\n')
    connection.close()

if __name__=='__main__':
    my_publish(binding_keys=[
        "celerity.color.animal",        # no. 0
        "quick.orange.rabbit",          # no. 1
        "lazy.orange.elephant",         # no. 2
        "quick.orange.fox",             # no. 3
        "lazy.brown.fox",               # no. 4
        "lazy.pink.rabbit",             # no. 5
        "quick.brown.fox",              # no. 6
        "orange",                       # no. 7
        "quick.orange.new.rabbit",      # no. 8
        "lazy.orange.new.rabbit",       # no. 9
    ])
    '''
    [no.1]: A message with a routing key set to quick.orange.rabbit will be delivered to both queues.
    [no.2]: Message lazy.orange.elephant also will go to both of them.
    [no.3]: On the other hand quick.orange.fox will only go to the first queue,
    [no.4]: and lazy.brown.fox only to the second.
    [no.5]: lazy.pink.rabbit will be delivered to the second queue only once, even though it matches two bindings.
    [no.6]: quick.brown.fox doesn't match any binding so it will be discarded.
    [no.7]: What happens if we break our contract and send a message with one or four words, like orange or
    [no.8]: quick.orange.new.rabbit? Well, these messages won't match any bindings and will be lost.
    [no.9]: On the other hand lazy.orange.new.rabbit, even though it has four words, will match the last binding and will be delivered to the second queue.
    '''