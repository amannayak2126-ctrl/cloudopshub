import logging

from config import LOG_FILE


def get_logger(name="cloudopshub"):
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
