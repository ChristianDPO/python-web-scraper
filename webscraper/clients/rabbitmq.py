import aio_pika
import asyncio
import json


class AsyncRabbitMQClient(object):
    """
    Asynchronous RabbitMQ client for publishing messages to a single queue
    """

    def __init__(self, url, queue_name):
        """
        :param str url: RabbitMQ connection URL
        :param str queue_name: Name of the queue for publishing/consuming messages
        :param aio_pika.RobustConnection connection: Active RabbitMQ connection
        :param aio_pika.Channel channel: Channel associated with the connection
        """

        self.url = url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def connect(self):
        """
        Connects to RabbitMQ instance asynchronously, if it's not alredy connected.
        Declares a new durbale queue it if does not exist.

        :return: None
        :rtype: None
        """

        if not self.connection:

            self.connection = await aio_pika.connect_robust(self.url)
            self.channel = await self.connection.channel()
            await self.channel.declare_queue(self.queue_name, durable=True)

    async def publish(self, body):
        """
        Publishes a message to the queue asynchronously.

        :param models.message_dto.QueueMessageDTO body: The message body to publish.
        :return: None
        :rtype: None
        """

        if not self.connection:
            await self.connect()

        message = aio_pika.Message(body.json().encode())
        await self.channel.default_exchange.publish(
            message, routing_key=self.queue_name
        )

    async def consume_forever(self, callback):
        """
        Listens and consumes the messages from the queue forever.

        :param callable callback: Async function to process each message (accepts dict)
        :return: None
        """

        if not self.connection:
            await self.connect()

        queue = await self.channel.get_queue(self.queue_name)

        try:

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        body = json.loads(message.body.decode())
                        await callback(body)

        except aio_pika.exceptions.AMQPConnectionError:
            # Tries to automatically reconnect
            await asyncio.sleep(5)
            await self.connect()

    async def close(self):
        """
        Closes the RabbitMQ connection asynchronously

        :return: None
        :rtype: None
        """

        if self.connection:
            await self.connection.close()
            self.connection = None
            self.channel = None
