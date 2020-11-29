from settings import LOG_LEVEL, LOG_FILE, LOG_FORMAT
import logging, sys

def get_logger():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE)
    stdout_handler = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger("task")
    logger.addHandler(stdout_handler)
    return logger