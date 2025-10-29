import asyncio
import logging
from webscraper.worker.worker import ScrapeWorker
from webscraper.config import Settings

from webscraper.helpers.log import Log


async def main():
    settings = Settings()
    Log.setup(logging.INFO)
    logger = Log.get_logger(__name__)

    logger.info("Starting Scrape Worker...")
    worker = ScrapeWorker(settings)
    await worker.start_worker()


if __name__ == "__main__":
    asyncio.run(main())
