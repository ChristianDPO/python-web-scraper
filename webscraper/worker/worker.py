import aio_pika
import asyncio
import pydantic

from webscraper.clients.rabbitmq import AsyncRabbitMQClient
from webscraper.clients.redis import AsyncRedisClient

from webscraper.models.message_dto import ScrapeJobMessageDTO
from webscraper.models.cache_dto import CacheMessageDTO

from webscraper.services.scrape import ScrapeService

from webscraper.helpers.log import Log

from webscraper.exceptions import InvalidRabbitMQMessageException


class ScrapeWorker(object):
    def __init__(self, settings):
        """
        Initialize the ScrapeWorker with application settings.

        :param webscraper.config.Settings settings: Application settings containing RabbitMQ,
        Redis and scrape configurations
        """

        self._rabbitmq_client = AsyncRabbitMQClient(
            settings.rabbitmq_url, settings.rabbitmq_queue
        )
        self._redis_client = AsyncRedisClient(settings.redis_url)
        self._scrape_service = ScrapeService(settings.scrape_url, self._redis_client)

        self.logger = Log.get_logger(__name__)

    async def start_worker(self):
        """
        Starts the worker to listen for scrape job messages from RabbitMQ and process them.

        :return: None
        """

        try:
            await self._rabbitmq_client.connect()
            await self._rabbitmq_client.consume_forever(self.process_message)
        except aio_pika.exceptions.AMQPConnectionError:
            self.logger.warning("Connection lost to RabbitMQ. Retrying in 5 seconds...")
            await asyncio.sleep(5)

    async def process_message(self, message_body):
        """
        Process a scrape job message.
        :param dict message_body: The message body returned by RabbitMQ.
        :raises webscraper.exceptions.InvalidRabbitMQMessageException: If the message format is invalid.
        Should be able to be translated to ScrapeJobMessageDTO
        """

        self.logger.info("Processing message:", message_body)

        try:
            message = ScrapeJobMessageDTO(**message_body)
        except pydantic.ValidationError:
            self.logger.error("Invalid message format:", message_body)
            raise InvalidRabbitMQMessageException("Invalid message format")

        await self._scrape_service.set_cache(
            message.cnpj, CacheMessageDTO(status="IN_PROGRESS")
        )

        try:
            data = await self._scrape_service.scrape(message.cnpj)
        except Exception as e:
            self.logger.error(f"Error scraping data for CNPJ {message.cnpj}: {e}")
            await self._scrape_service.set_cache(
                message.cnpj, CacheMessageDTO(status="FAILED", data={str(e)})
            )
            return

        self.logger.info(f"Scraped data for CNPJ {message.cnpj}: {data}")
        await self._scrape_service.set_cache(
            message.cnpj, CacheMessageDTO(status="COMPLETED", data=data)
        )
