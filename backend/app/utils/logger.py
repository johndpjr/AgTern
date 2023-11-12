import logging
import logging.handlers
import time
from os import getpid, makedirs
from pathlib import Path


def setup_logger(name):
    # logger settings
    makedirs(Path.cwd().joinpath("log"), exist_ok=True)
    file = "log/agtern.log.{}.{}".format(
        time.strftime("(%Y-%m-%d)-(%H-%M-%S)"), getpid()
    )
    format = "%(asctime)s [%(levelname)s] %(message)s"

    # setup handlers and formatters
    rotate_handler = logging.handlers.TimedRotatingFileHandler(
        file, when="midnight", interval=1, backupCount=7
    )
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(format)

    # attach handlers to logger
    logger = logging.getLogger(name)
    console_handler.setFormatter(log_formatter)
    rotate_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    logger.addHandler(rotate_handler)

    return logger


LOG = setup_logger("root")
