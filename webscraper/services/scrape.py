from playwright.async_api import async_playwright

from webscraper.models.cache_dto import CacheMessageDTO


class ScrapeService(object):
    """
    Service class for web scraping using Playwright.
    """

    SCRAPE_JOB_REDIS_PREFIX = "scrape_job:"
    DEFAULT_SCRAPE_CACHE_TTL = "3600"

    def __init__(self, scrape_url, redis_client=None):
        """
        Initialize the ScrapeService with the URL to scrape.

        :param str scrape_url: URL of the page to scrape
        :param webscraper.clients.redis.AsynchRedisClient: An optional Redis client for caching results
        :rtype: None
        """
        self.scrape_url = scrape_url
        self._redis_client = redis_client

    async def scrape(self, cnpj):
        """
        Perform a web scraping job for a given CNPJ.

        This method opens the target page using Playwright, fills the CNPJ form,
        submits it, waits for the results, and extracts key-value pairs
        from the resulting document.

        :param str cnpj: The CNPJ number to be searched on the page
        :return: A dictionary mapping field titles to their corresponding values
        :rtype: dict
        """
        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(self.scrape_url)
            await page.click("input#rTipoDocCNPJ")
            await page.fill("input#tCNPJ", cnpj)
            await page.click('input[name="btCGC"][type="submit"]')
            await page.wait_for_selector("div.container.doc", state="visible")

            items = await page.query_selector_all("div.item, div.col.box")
            data = {}

            for item in items:

                title_el = await item.query_selector(
                    "span.label_title, div.label_title"
                )
                value_el = await item.query_selector("span.label_text")

                title = await title_el.text_content() if title_el else None
                value = await value_el.text_content() if value_el else None

                if title and value:
                    data[title.strip()] = value.strip()

            await browser.close()
            return data

    async def set_cache(self, cnpj, cache):
        """
        Caches the scraped data in Redis with a key based on the CNPJ.

        :param str cnpj: The CNPJ number
        :param webscraper.models.cache_dto.CacheMessageDTO cache: The scraped data to cache
        """
        if self._redis_client:
            key = f"{self.SCRAPE_JOB_REDIS_PREFIX}{cnpj}"
            await self._redis_client.set_value(key, cache.model_dump(), ttl=3600)

    async def get_cache(self, cnpj):
        """
        Retrieves cached scraped data from Redis for a given CNPJ.

        :param str cnpj: The CNPJ number
        :return: The cached scraped data if available, None otherwise
        :rtype: webscraper.models.cache_dto.CacheMessageDTO | None
        """
        if self._redis_client:
            key = f"{self.SCRAPE_JOB_REDIS_PREFIX}{cnpj}"
            cache = await self._redis_client.get_value(key)
            if cache:
                return CacheMessageDTO(**cache)
        return None
