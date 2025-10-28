from playwright.async_api import async_playwright


class ScrapeWorker(object):
    def __init__(self, name):
        self.name = name

    async def scrape(self, cnpj):

        async with async_playwright() as p:

            browser = await p.chromium.launch(headless=True)

            page = await browser.new_page()

            await page.goto(
                "https://appasp.sefaz.go.gov.br/Sintegra/Consulta/default.html"
            )

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
