from pydantic import BaseModel


class QueueMessageDTO(BaseModel):
    """
    Base DTO for messages in the RabbitMQ queue.

    :param job: The type of job (e.g., 'SCRAPE')
    :param status: Status of the job (e.g., 'QUEUED', 'PROCESSING', 'DONE')
    """

    job: str
    status: str


class ScrapeJobMessageDTO(QueueMessageDTO):
    """
    DTO for a scraping job message. Extends QueueMessageDTO.

    :param cnpj: CNPJ of the company to scrape
    """

    job: str = "SCRAPE"
    status: str = "QUEUED"
    cnpj: str
