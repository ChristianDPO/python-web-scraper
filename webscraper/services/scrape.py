from webscraper.clients.rabbitmq import AsyncRabbitMQClient
from playwright.async_api import async_playwright


class ScrapeService(object):
    """
    Service responsible for creating scraping jobs and sending them to RabbitMQ.
    """

    def __init__(self, scrape_url, rabbitmq_url, rabbitmq_queue):
        """
        Initialize the ScrapeService with URLs and RabbitMQ queue info.

        :param scrape_url: URL of the page to scrape (not used in this snippet but may be for worker)
        :param rabbitmq_url: Connection URL for RabbitMQ
        :param rabbitmq_queue: Name of the RabbitMQ queue to publish messages to
        """

        self.scrape_url = scrape_url
        self.rabbitmq_url = rabbitmq_url
        self.rabbitmq_queue = rabbitmq_queue
        self.rabbitmq_client = AsyncRabbitMQClient(rabbitmq_url, rabbitmq_queue)

    async def scrape(self, cnpj):

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)

            page = await browser.new_page()

            await page.goto(self.scrape_url)

            await page.click("input#rTipoDocCNPJ")

            await page.fill("input#tCNPJ", cnpj)

            await page.click('input[name="btCGC"][type="submit"]')

            await page.wait_for_selector("div.container.doc", state="visible")

            items = await page.query_selector_all("div.item")
            data = {}

            for item in items:

                title_el = await item.query_selector("span.label_title")
                value_el = await item.query_selector("span.label_text")

                title = await title_el.text_content() if title_el else None
                value = await value_el.text_content() if value_el else None

                if title and value:
                    data[title.strip()] = value.strip()

            await browser.close()
            return data
