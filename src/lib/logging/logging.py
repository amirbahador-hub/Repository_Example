import atexit
import json
import yaml
import logging.config
import logging.handlers
import pathlib


def setup_logging():
    config_file = pathlib.Path("config/logging.yml")
    with open(config_file) as f_in:
        # config = json.load(f_in)
        config = yaml.safe_load(f_in)

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)
