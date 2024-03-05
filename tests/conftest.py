from tenacity import retry, stop_after_delay
from lib.config import get_config
import requests
import redis
import pytest


@retry(stop=stop_after_delay(10))
def wait_for_webapp_to_come_up():
    return requests.get(get_config("app_url"))

@retry(stop=stop_after_delay(10))
def wait_for_redis_to_come_up():
    r = redis.Redis(**get_config("redis"))
    return r.ping()

@pytest.fixture
def async_redis():
    return redis.asyncio.Redis(**get_config("redis"))


@pytest.fixture
def restart_redis_pubsub():
    wait_for_redis_to_come_up()

@pytest.fixture
def restart_api():
    wait_for_webapp_to_come_up()