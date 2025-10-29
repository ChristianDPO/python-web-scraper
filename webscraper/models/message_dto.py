import re
import pydantic


class QueueMessageDTO(pydantic.BaseModel):
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

    @pydantic.field_validator("cnpj", mode="before")
    def sanitize_cnpj(cls, v):
        """
        Remove all non-digit characters from the CNPJ and validate its length.
        :raises: ValueError if invalid.
        """
        cnpj_digits = re.sub(r"\D", "", v)
        if len(cnpj_digits) != 14:
            raise ValueError(f"Invalid CNPJ: {v}")
        return cnpj_digits
