import aio_pika
import asyncio
import json

from webscraper.helpers.log import Log


class AsyncRabbitMQClient(object):
    """
    Asynchronous RabbitMQ client for publishing messages to a single queue.
    """

    def __init__(self, url, queue_name):
        """
        :param str url: RabbitMQ connection URL
        :param str queue_name: Name of the queue for publishing/consuming messages
        :rtype: None
        """
        self.url = url
        self.queue_name = queue_name
        self._connection = None
        self.logger = Log.get_logger(__name__)

    async def connect(self):
        """
        Connects to RabbitMQ instance asynchronously, if it's not already connected.
        Declares a new durable queue if it does not exist.

        :rtype: None
        """
        if not self._connection:
            self._connection = await aio_pika.connect_robust(self.url)
            async with self._connection.channel() as channel:
                await channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, body):
        """
        Publishes a message to the queue asynchronously.

        :param webscraper.models.message_dto.QueueMessageDTO body: The message body to publish
        :rtype: None
        """
        await self.connect()
        message = aio_pika.Message(body.json().encode())

        async with self._connection.channel() as channel:
            await channel.default_exchange.publish(message, routing_key=self.queue_name)

        self.logger.info(f"Sent message: {body.model_dump()}")

    async def consume_forever(self, callback):
        """
        Listens and consumes the messages from the queue forever.
        Tries to reconnect automatically on connection errors.

        :param callable(dict) callback: Async function to process each message.
                                         Needs to accept a dict (message body) as parameter.
        :rtype: None
        """
        await self.connect()

        channel = await self._connection.channel()
        queue = await channel.get_queue(self.queue_name)

        while True:
            try:
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            body = json.loads(message.body.decode())
                            self.logger.info(f"Received message: {body}")
                            try:
                                await callback(body)
                            except Exception as e:
                                self.logger.exception(f"Error processing message: {e}")

            except aio_pika.exceptions.AMQPConnectionError:
                # Tries to automatically reconnect
                await asyncio.sleep(5)
                await self.connect()

    async def close(self):
        """
        Closes the RabbitMQ connection asynchronously.

        :rtype: None
        """
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
            self._connection = None
