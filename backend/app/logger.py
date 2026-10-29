# log along with timestamp
# in logger we can give format we want

import logging, sys


def get_logger(name):
    # for which file it gonna print is the "name" here
    logger = logging.getLogger(name)
    # setlevel - error , debug, exception ,warning
    logger.setLevel(logging.INFO)
    handlers = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handlers.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handlers)

    return logger

