from redis.asyncio import Redis as AsyncRedis
from lib.config import get_config
from functools import partial
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from similarity.services import handlers, messagebus, unit_of_work
from similarity.adapters import repository


class Container(DeclarativeContainer):
    redis = Singleton(AsyncRedis, **get_config("redis"))


    # Unit Of Work
    knowledge_base_persistence_unit_of_work = Factory(unit_of_work.KnowledgeBasePersistenceUnitOfWork, engine=redis)

    # handlers
    injected_command_handlers = dict() 
    for command_type, handlers in handlers.COMMAND_HANDLERS.items():
        injected_command_handlers[command_type] = partial(handlers, uow=knowledge_base_persistence_unit_of_work())

    # bus
    knowledge_base_bus = Factory(messagebus.MessageBus, uow=knowledge_base_persistence_unit_of_work(), command_handlers=injected_command_handlers, event_handlers={})