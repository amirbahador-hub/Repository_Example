import json
import logging
from dataclasses import asdict
import redis

from lib.config import get_config
from similarity.domain import events

logger = logging.getLogger(__name__)

r = redis.Redis(**get_config("redis"))


def publish(channel, event: events.Event):
    logging.info("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event)))
