import json
import logging
import asyncio
import redis

from similarity.domain import commands
from similarity.services.messagebus import MessageBus
from similarity.container import Container
from fastapi import Depends
from dependency_injector.wiring import Provide, inject


logger = logging.getLogger(__name__)


@inject
async def main(
    bus: MessageBus = Depends(Provide[Container.document_faiss_bus]),
    redis: redis.asyncio.Redis= Depends(Provide[Container.redis])
):
    print("Redis pubsub setting up ...")
    pubsub = redis.pubsub(ignore_subscribe_messages=True)
    await pubsub.psubscribe("document.*"),
    print("Redis waiting for messages ...")
    async for message in pubsub.listen():
        await handle_document_change(message, bus)


async def handle_document_change(m, bus):
    print(f"handling {m}")
    logger.info("handling %s", m)
    data, channel = m["data"], m["channel"]
    data = json.loads(data)
    if channel == "document.add":
        cmd = commands.AddDocument(**data)
    elif channel == "document.remove":
        cmd = commands.RemoveDocument(**data)
    await bus.handle(cmd)