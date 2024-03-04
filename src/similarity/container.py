from redis.asyncio import StrictRedis as AsyncRedis
from lib.config import get_config
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from similarity.adapters.faiss_db import FaissOrm
from similarity.adapters.redis_db import RedisAdapter
from similarity.services import handlers, messagebus, unit_of_work


class Container(DeclarativeContainer):
    redis = Singleton(AsyncRedis, **get_config("redis"))
    db = Singleton(FaissOrm)

    redis_adapter = Factory(RedisAdapter, redis)

    # Unit Of Work
    knowledge_base_persistence_unit_of_work = Factory(
        unit_of_work.KnowledgeBasePersistenceUnitOfWork, adapter=redis_adapter
    )
    document_redis_unit_of_work = Factory(
        unit_of_work.DocumentPersistenceUnitOfWork, adapter=redis_adapter
    )
    document_faiss_unit_of_work = Factory(
        unit_of_work.DocumentPersistenceUnitOfWork, adapter=db
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
    document_faiss_bus = Factory(
        messagebus.MessageBus,
        uow=document_faiss_unit_of_work(),
        command_handlers=handlers.COMMAND_HANDLERS,
        event_handlers=handlers.EVENT_HANDLERS,
    )