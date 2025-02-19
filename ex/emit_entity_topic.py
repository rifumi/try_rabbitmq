import json
from aio_pika import ExchangeType

from ex import EXCHANGE_NAME
from utils.get_connection import get_connection


def my_publish(binding_keyvalues: list[tuple[str, dict]]):
    connection = get_connection()
    channel = connection.channel()

    exchange_name = EXCHANGE_NAME
    channel.exchange_declare(exchange=exchange_name,
                             exchange_type=ExchangeType.TOPIC)

    for counter, routing_kv in enumerate(binding_keyvalues):
        ''' routing_key: <entity>.<event> '''
        routing_key = routing_kv[0]
        value = routing_kv[1]
        message = {
            "args": value,
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


if __name__ == '__main__':
    my_publish(
        binding_keyvalues=[
            (
                "entity.event",
                {"value": "blank"}
            ),        # no. 0
            (
                "user.created",
                {
                    "userId": "12345",
                    "userName": "John Doe",
                    "email": "john.doe@example.com",
                    "timestamp": "2025-02-18T04:56:07Z"
                }
            ),        # no. 1
            (
                "user.updated",
                {
                    "userId": "12345",
                    "updatedFields": {
                        "userName": "John Doe",
                        "email": "john.doe@newdomain.com"
                    },
                    "timestamp": "2025-02-18T05:00:00Z"
                }
            ),        # no. 2
            (
                "user.deleted",
                {
                    "userId": "12345",
                    "timestamp": "2025-02-18T05:05:00Z"
                }
            ),                                                  # no. 3
            (
                "circle.created",
                {
                    "circleId": "67890",
                    "circleName": "Tech Enthusiasts",
                    "createdBy": "12345",
                    "timestamp": "2025-02-18T06:00:00Z"
                }
            ),          # no. 4
            (
                "circle.updated",
                {
                    "circleId": "67890",
                    "updatedFields": {
                        "circleName": "Tech Innovators"
                    },
                    "timestamp": "2025-02-18T06:05:00Z"
                }
            ),   # no. 5
            (
                "circle.deleted",
                {
                    "circleId": "67890",
                    "timestamp": "2025-02-18T06:10:00Z"
                }
            ),          # no. 6
        ])
