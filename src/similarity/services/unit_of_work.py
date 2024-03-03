from redis.asyncio import Redis as AsyncRedis
from similarity.adapters.repository import RedisRepository
import dependency_injector
from typing import Protocol


class AbstractUnitOfWork(Protocol):
    def __init__(self, engine) -> None:
        ...

    async def __aenter__(self) -> None:
        ...


class KnowledgeBasePersistenceUnitOfWork:
    def __init__(self, engine: AsyncRedis) -> None:
        self.engine = engine
        self.repository = RedisRepository(engine)

    async def __aenter__(self,*args ,**kwargs) -> None:
        for repo_name, repo_factory in self.repo_factories.items():
            self.__setattr__(
                repo_name,
                repo_factory(redis=self.engine),
            )

    async def __aexit__(self, *args, **kwargs) -> None:
        ...