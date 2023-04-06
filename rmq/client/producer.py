import asyncio
import logging

from client import Client


def run():
    rmq_client = Client()
    logging.info('rabbitmq client initialized')
    asyncio.run(
        rmq_client.publish(
            body={'python': 'test'},
            routing_key='test',
        ),
    )


def main():
    run()


if __name__ == '__main__':
    main()
