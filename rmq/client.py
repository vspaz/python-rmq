import asyncio
import logging

import ujson
from aio_pika import DeliveryMode, ExchangeType, Message, connect

from .__version__ import __version__


class Client:
    def __init__(self, config):
        self._config = config
        self._conn = f"amqp://{config.user}:{config.password}@{config.host}:{config.port}/"
        logging.info("client '%s' initialized: ok", __version__)

    async def _establish_connection(self):
        return await connect(
            url=self._conn,
            loop=asyncio.get_running_loop(),
            timeout=self._config.connection_timeout,
        )

    async def subscribe(self, queue_name, on_message):
        connection = await self._establish_connection()
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=8)
        queue = await channel.declare_queue(queue_name, durable=True)
        logging.info(f"queue '{queue_name}' starting to consume messages")
        await queue.consume(on_message)

    async def publish(self, body, routing_key):
        connection = await self._establish_connection()
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name="test",
            type=ExchangeType.DIRECT,
            durable=True,
        )
        queue = await channel.declare_queue(name="test", durable=True)
        await queue.bind(exchange=exchange)
        message = Message(
            body=ujson.dumps(obj=body).encode(),
            content_type="application/json",
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await exchange.publish(
            message=message,
            routing_key=routing_key,
        )
        logging.debug(f"sent: {message!r}")
        await connection.close()
        return dict(status="accepted")
