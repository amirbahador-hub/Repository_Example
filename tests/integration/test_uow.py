import uuid
import pytest
from similarity.adapters.redis_db import RedisAdapter
from similarity.domain.types import DocumentId, KnowledgeBaseName
from similarity.domain.models import Document, KnowledgeBase
from similarity.services.unit_of_work import DocumentPersistenceUnitOfWork, KnowledgeBasePersistenceUnitOfWork
from ..random_refs import random_content, random_knowledge_base


@pytest.mark.asyncio
async def test_uow_happy_path(async_redis):

    adapter = RedisAdapter(async_redis)

    knowledge_base = KnowledgeBase(name= KnowledgeBaseName(random_knowledge_base()))
    document = Document(id=DocumentId(uuid.uuid4()),content=random_content())

    uow = KnowledgeBasePersistenceUnitOfWork(adapter)
    async with uow:
        await uow.repository.add(knowledge_base)

    uow = DocumentPersistenceUnitOfWork(adapter)

    async with uow:
        await uow.repository.add(document, knowledge_base.name)
        response = await uow.repository.delete(document.id, knowledge_base.name)

    assert response == document.id
