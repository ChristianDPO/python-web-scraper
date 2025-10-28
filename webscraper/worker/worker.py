class ScrapeWorker(object):
    def __init__(self, scrape_service):
        """
        :param ScrapeService scrape_service: Instance of ScrapeService to perform scraping tasks
        """
        self.scrape_service = scrape_service
