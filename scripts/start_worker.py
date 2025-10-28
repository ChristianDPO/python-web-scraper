import asyncio
from pprint import pprint
from webscraper.worker.worker import ScrapeWorker


async def start():

    worker = ScrapeWorker(name="Worker1")

    results = await asyncio.gather(
        worker.scrape("00022244000175"),
        worker.scrape("00012377000160"),
        worker.scrape("00006486000175"),
    )

    for result in results:
        pprint(result)


if __name__ == "__main__":
    asyncio.run(start())
