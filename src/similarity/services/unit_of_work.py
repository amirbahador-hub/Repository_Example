from redis.asyncio import Redis as AsyncRedis
from similarity.adapters.repositories import DocumentRepository, KnowledgeBaseRepository
from similarity.adapters.redis_db import RedisAdapter
from typing import Protocol, Union


class AbstractUnitOfWork(Protocol):
    repository: Union[KnowledgeBaseRepository, DocumentRepository]

    def __init__(self, engine) -> None: ...

    async def __aenter__(self) -> None: ...

    async def __aexit__(self, *args) -> None: ...


class KnowledgeBasePersistenceUnitOfWork:
    repository: KnowledgeBaseRepository

    def __init__(self, engine: AsyncRedis) -> None:
        self.engine = engine

    async def __aenter__(self) -> None:
        assert isinstance(self.engine, AsyncRedis)
        adapter = RedisAdapter(self.engine)
        self.repository = KnowledgeBaseRepository(adapter)

    async def __aexit__(self, *args) -> None: ...


class DocumentPersistenceUnitOfWork:
    repository: DocumentRepository

    def __init__(self, engine: AsyncRedis) -> None:
        self.engine = engine

    async def __aenter__(self) -> None:
        if isinstance(self.engine, AsyncRedis):
            adapter = RedisAdapter(self.engine)
            self.repository = DocumentRepository(adapter)
        ...

    async def __aexit__(self, *args) -> None: ...
