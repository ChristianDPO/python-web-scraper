import sys
import logging


class Log(object):
    """
    A simple logger class to log messages with different severity levels.
    """

    LOG_FORMATTER = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    @staticmethod
    def setup(logger_level=logging.WARNING, stdout_log=True):
        """
        Sets up the logger with the specified level and output options.

        :param logger_level: Logging level (e.g., logging.INFO, logging.DEBUG)
        :param stdout_log: If True, logs will be printed to standard output
        """

        root_logger = logging.getLogger()
        root_logger.setLevel(logger_level)

        if not root_logger.hasHandlers():
            if stdout_log:
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logger_level)
                handler.setFormatter(logging.Formatter(Log.LOG_FORMATTER))
            # TODO: Add file handler here if needed

            root_logger.addHandler(handler)

    @staticmethod
    def get_logger(name="default"):
        """
        Returns a configured logger instance.

        :param name: Name of the logger
        :return: Configured logger instance
        :rtype: logging.Logger
        """

        logger = logging.getLogger()
        if not logger.hasHandlers():
            Log.setup(logger_level=logging.INFO, stdout_log=True)

        return logging.getLogger(name)
