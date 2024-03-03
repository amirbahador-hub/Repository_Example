from redis.asyncio import Redis as AsyncRedis
from lib.config import get_config
from functools import partial
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from similarity.services import handlers, messagebus, unit_of_work


class Container(DeclarativeContainer):
    redis = Singleton(AsyncRedis, **get_config("redis"))

    # Unit Of Work
    knowledge_base_persistence_unit_of_work = Factory(
        unit_of_work.KnowledgeBasePersistenceUnitOfWork, engine=redis
    )
    document_redis_unit_of_work = Factory(
        unit_of_work.DocumentPersistenceUnitOfWork, engine=redis
    )

    # bus
    knowledge_base_bus = Factory(
        messagebus.MessageBus,
        uow=knowledge_base_persistence_unit_of_work(),
        command_handlers=handlers.COMMAND_HANDLERS,
        event_handlers=handlers.EVENT_HANDLERS,
    )
    document_bus = Factory(
        messagebus.MessageBus,
        uow=document_redis_unit_of_work(),
        command_handlers=handlers.COMMAND_HANDLERS,
        event_handlers=handlers.EVENT_HANDLERS,
    )
