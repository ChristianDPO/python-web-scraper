from webscraper.clients.rabbitmq import AsyncRabbitMQClient
from webscraper.clients.redis import AsyncRedisClient

from webscraper.models.message_dto import ScrapeJobMessageDTO
from webscraper.models.cache_dto import CacheMessageDTO

from webscraper.services.scrape import ScrapeService

from webscraper.helpers.log import Log


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

        await self._rabbitmq_client.connect()

        while True:

            await self._rabbitmq_client.consume_forever(self.process_message)

    async def process_message(self, message_body):
        """
        Process a scrape job message.
        :param dict message_body: The message body returned by RabbitMQ.
        Should be able to be translated to ScrapeJobMessageDTO
        """

        self.logger.info("Processing message:", message_body)
        message = ScrapeJobMessageDTO(**message_body)

        cache = CacheMessageDTO(status="IN_PROGRESS")
        await self._scrape_service.set_cache(message.cnpj, cache)

        data = await self._scrape_service.scrape(message.cnpj)
        self.logger.info(f"Scraped data for CNPJ {message.cnpj}: {data}")

        if data:
            cache = CacheMessageDTO(status="COMPLETED", data=data)
            await self._scrape_service.set_cache(message.cnpj, cache)
