import asyncio

import uvloop
from config import Config

from rmq.client import Client

uvloop.install()


def run():
    rmq_client = Client(config=Config())
    asyncio.run(
        rmq_client.publish(
            body={"python": "test"},
            routing_key="test",
        ),
    )


def main():
    run()


if __name__ == "__main__":
    main()
