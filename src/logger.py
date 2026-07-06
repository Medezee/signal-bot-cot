import logging


def setup_logger(name: str, level: logging._Level):
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s %(name)s [%(levelname)s] - %(funcName)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
