from playwright.async_api import async_playwright


class ScrapeService(object):
    """
    Service class for web scraping using Playwright.
    """

    def __init__(self, scrape_url):
        """
        Initialize the ScrapeService with the URL to scrape.

        :param str scrape_url: URL of the page to scrape
        :rtype: None
        """
        self.scrape_url = scrape_url

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
