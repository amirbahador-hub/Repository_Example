import json
import logging
import asyncio
import redis

from similarity.domain import commands
from similarity.services.messagebus import MessageBus
from fastapi import Depends
from dependency_injector.wiring import Provide, inject
from similarity.views import similarity
from redis.asyncio import StrictRedis as AsyncRedis
from lib.config import get_config
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from similarity.adapters.faiss_db import FaissOrm
from similarity.services import handlers, messagebus, unit_of_work


logger = logging.getLogger(__name__)


class MQContainer(DeclarativeContainer):
    redis = Singleton(AsyncRedis, **get_config("redis"))
    db = Singleton(FaissOrm)
    document_faiss_unit_of_work = Factory(
        unit_of_work.DocumentPersistenceUnitOfWork, adapter=db
    )
    document_faiss_bus = Factory(
        messagebus.MessageBus,
        uow=document_faiss_unit_of_work(),
        command_handlers=handlers.COMMAND_HANDLERS,
        event_handlers=handlers.EVENT_HANDLERS,
    )


@inject
async def main(
    bus: MessageBus = Depends(Provide[MQContainer.document_faiss_bus]),
    redis: redis.asyncio.Redis = Depends(Provide[MQContainer.redis]),
):
    print("Redis pubsub setting up ...")
    pubsub = redis.pubsub(ignore_subscribe_messages=True)
    await pubsub.psubscribe("document.*"),
    print("Redis waiting for messages ...")
    async for message in pubsub.listen():
        await handle_document_change(message, bus, redis)


async def handle_document_change(m, bus, redis):
    print(f"handling {m}")
    logger.info("handling %s", m)
    data, channel = m["data"], m["channel"]
    data = json.loads(data)
    if channel == "document.add":
        cmd = commands.AddDocument(**data)
        await bus.handle(cmd)
    elif channel == "document.remove":
        cmd = commands.RemoveDocument(**data)
        await bus.handle(cmd)
    elif channel == "document.get":
        response = await similarity(
            content=data["query"], name=data["name"], uow=bus.uow
        )
        print(response)
        await redis.rpush(
            data["key"],
            json.dumps([{"content": res.content, "id": res.id} for res in response]),
        )
        await redis.expire(data["key"], 10)
