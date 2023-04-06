import json
import logging

import aiomisc
import uvloop
from aio_pika import IncomingMessage
from client import Client

uvloop.install()


async def listen_for_messages(rmq_client: Client):
    async def on_message_received(message: IncomingMessage):
        async with message.process(requeue=True):
            try:
                resp = json.loads(message.body)
                logging.error(f"message received: {resp!r}")
            except Exception as err:
                logging.error(err)

    await rmq_client.subscribe(
        queue_name="test",
        on_message=on_message_received,
    )


def run():
    with aiomisc.entrypoint() as loop:
        rmq_client = Client()
        logging.info("rabbitmq client initialized")
        loop.create_task(listen_for_messages(rmq_client=rmq_client))
        loop.run_forever()


def main():
    run()


if __name__ == "__main__":
    main()
