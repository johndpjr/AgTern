import logging
import logging.handlers
from os import makedirs
from pathlib import Path

from .pipelines.data import DataFile


def setup_logger(name):
    # logger settings
    makedirs(Path.cwd().joinpath("log"), exist_ok=True)
    file = "log/agtern.log"
    format = "%(asctime)s [%(levelname)s] %(message)s"

    # setup handlers and formatters
    rotateHandler = logging.handlers.TimedRotatingFileHandler(
        file, when="midnight", interval=1, backupCount=7
    )
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(format)

    # attach handlers to logger
    logger = logging.getLogger(name)
    consoleHandler.setFormatter(logFormatter)
    rotateHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)
    logger.addHandler(rotateHandler)

    return logger


LOG = setup_logger("root")
