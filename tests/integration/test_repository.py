import uuid
import pytest
from similarity.adapters.repositories import DocumentRepository, KnowledgeBaseRepository
from similarity.adapters.redis_db import RedisAdapter
from similarity.domain.types import DocumentId, KnowledgeBaseName
from similarity.domain.models import Document, KnowledgeBase
from similarity.domain.exceptions import InvalidDocument, InvalidKnowledgeBaseName
from ..random_refs import random_content, random_knowledge_base


@pytest.mark.asyncio
async def test_add_document_invalid_knowledge_base(async_redis):
    adapter = RedisAdapter(async_redis)
    document_repository = DocumentRepository(adapter)
    knowledge_base_name = KnowledgeBaseName(random_knowledge_base())
    document = Document(
        id=DocumentId(uuid.uuid4()),
        content=random_content(),
    )

    with pytest.raises(InvalidKnowledgeBaseName):
        await document_repository.add(document=document, name=knowledge_base_name)


@pytest.mark.asyncio
async def test_invalid_document_removal(async_redis):

    adapter = RedisAdapter(async_redis)
    document_repository = DocumentRepository(adapter)
    knowledge_base_repository = KnowledgeBaseRepository(adapter)

    knowledge_base = KnowledgeBase(
        name= KnowledgeBaseName(random_knowledge_base())
    )
    await knowledge_base_repository.add(knowledge_base=knowledge_base)
    with pytest.raises(InvalidDocument):
        await document_repository.delete(id=uuid.uuid4(), name=knowledge_base.name)


@pytest.mark.asyncio
async def test_add_document(async_redis):
    adapter = RedisAdapter(async_redis)
    document_repository = DocumentRepository(adapter)
    knowledge_base_repository = KnowledgeBaseRepository(adapter)

    knowledge_base = KnowledgeBase(
        name= KnowledgeBaseName(random_knowledge_base())
    )
    document = Document(
        id=DocumentId(uuid.uuid4()),
        content=random_content(),
    )
    await knowledge_base_repository.add(knowledge_base=knowledge_base)
    await document_repository.add(document=document, name=knowledge_base.name)
       
    assert str(document.id) in await knowledge_base_repository.get(knowledge_base.name)