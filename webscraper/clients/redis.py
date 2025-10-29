import json
import redis.asyncio as redis
from webscraper.helpers.log import Log


class AsyncRedisClient:
    """
    Asynchronous Redis client for storing and retrieving JSON-serializable objects.
    """

    def __init__(self, url):
        """
        Initialize the Redis client.

        :param str url: Redis connection URL
        :rtype: None
        """
        self.url = url
        self._redis = None
        self.logger = Log.get_logger(__name__)

    async def connect(self):
        """
        Connects to the Redis server asynchronously if not already connected.

        :rtype: None
        """
        if not self._redis:
            self._redis = await redis.from_url(self.url)

    async def set_value(self, key, value, ttl=None):
        """
        Stores a JSON-serializable object in Redis with an optional expiration time.

        :param str key: Redis key
        :param dict value: Python dictionary (or JSON-serializable object) to store
        :param int ttl: Expiration time in seconds. Defaults to None (no expiration).
        :rtype: None
        """
        await self.connect()
        data = json.dumps(value)
        await self._redis.set(key, data, ex=ttl)
        self.logger.info(f"Stored key '{key}' in Redis data '{data}'")

    async def get_value(self, key):
        """
        Retrieves a JSON object from Redis by key.

        :param str key: Redis key
        :return: Python dictionary if key exists, None otherwise
        :rtype: dict | None
        """
        await self.connect()
        data = await self._redis.get(key)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                self.logger.error(f"Failed to decode JSON for key '{key}'")
                return None
        return None

    async def close(self):
        """
        Closes the Redis connection.

        :rtype: None
        """
        if self._redis:
            await self._redis.close()
            self._redis = None
