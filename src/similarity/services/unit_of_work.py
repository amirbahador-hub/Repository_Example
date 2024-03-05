from redis.asyncio import Redis as AsyncRedis
from similarity.adapters.faiss_db import FaissOrm
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

    def __init__(self, adapter) -> None:
        self.adapter = adapter

    async def __aenter__(self) -> None:
        self.repository = KnowledgeBaseRepository(self.adapter)

    async def __aexit__(self, *args) -> None: ...


class DocumentPersistenceUnitOfWork:
    repository: DocumentRepository

    def __init__(self, adapter) -> None:
        self.adapter = adapter

    async def __aenter__(self) -> None:
        self.repository = DocumentRepository(self.adapter)

    async def __aexit__(self, *args) -> None: ...
