from lib.config import get_config
from lib.logging import setup_logging
import logging


setup_logging()
logger = logging.getLogger("my_app")  # __name__ is a common choice

print("HELLO", get_config("name"))
logger.debug("debug message", extra={"x": "hello"})
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("exception message")