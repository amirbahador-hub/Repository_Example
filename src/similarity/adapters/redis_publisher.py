import json
import logging
from dataclasses import asdict
import redis

from similarity.services.messagebus import Message
from similarity.container import APIContainer as Container
from fastapi import Depends
from dependency_injector.wiring import Provide, inject


logger = logging.getLogger(__name__)


@inject
async def publish(
    channel,
    message: Message | dict,
    redis: redis.asyncio.Redis = Depends(Provide[Container.redis]),
):
    print(f"publishing: channel={channel}, event={message}")
    if isinstance(message, Message):
        await redis.publish(channel, message.json())
    else:
        await redis.publish(channel, json.dumps(message))