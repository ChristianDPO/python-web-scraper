import asyncio
from pprint import pprint
from webscraper.worker.worker import ScrapeWorker


async def start():

    worker = ScrapeWorker(name="Worker1")
    cnpj_to_scrape = "00022244000175"  # Example CNPJ number
    result = await worker.scrape(cnpj_to_scrape)
    pprint(result)


if __name__ == "__main__":
    asyncio.run(start())
