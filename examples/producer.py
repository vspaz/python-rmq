import asyncio

import uvloop

from rmq.client import Client
from config import Config

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
