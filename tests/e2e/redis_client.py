import redis

from lib.config import get_config 

r = redis.Redis(**get_config("redis"))


def subscribe_to(channel):
    pubsub = r.pubsub()
    pubsub.psubscribe(channel)
    confirmation = pubsub.get_message(timeout=10)
    # assert confirmation["type"] == "subscribe"
    return pubsub
