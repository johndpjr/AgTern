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

    # setup logger
    logging.basicConfig(filename=file, format=format, filemode="a", level=logging.INFO)
    rotate_file = logging.handlers.TimedRotatingFileHandler(
        file, when="midnight", interval=1, backupCount=7
    )
    logger = logging.getLogger(name)
    logger.addHandler(rotate_file)

    # print log messages to console
    consoleHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(format)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger


LOG = setup_logger("root")
