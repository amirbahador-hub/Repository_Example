from redis.asyncio import Redis as AsyncRedis
from similarity.domain.exceptions import InvalidKnowledgeBaseName, InvalidDocument
from similarity.domain.models import Document
from similarity.domain.types import DocumentId, KnowledgeBaseName


class RedisAdapter:
    def __init__(self, redis: AsyncRedis):
        self.redis = redis

    async def add_knowledge_base(self, name: KnowledgeBaseName):
        await self.add_or_update_knowledge_base(name)

    async def add_or_update_knowledge_base(
        self, name: KnowledgeBaseName, ids: list[DocumentId] | None = None
    ):
        if ids is None:
            ids = await self.get_documents(name)
            ids = ids if ids is not None else []
        await self.redis.json().set(
            f"knowledge_bases:{name}", ".", [str(id) for id in ids]
        )

    async def delete_knowledge_base(self, name: KnowledgeBaseName):
        await self.validate_knowledge_base(name)
        await self.redis.json().delete(f"knowledge_bases:{name}")

    async def add_document(self, document: Document, name: KnowledgeBaseName):
        ids = await self.validate_knowledge_base(name)
        document_id = str(document.id)
        if document_id not in ids:
            await self.add_or_update_knowledge_base(name, ids + [document_id])

    async def delete_document(self, document_id: DocumentId, name: KnowledgeBaseName):
        ids = await self.validate_knowledge_base(name)
        document_id = str(document_id)
        if document_id in ids:
            ids.remove(document_id)
            await self.add_or_update_knowledge_base(name, ids)
        else:
            raise InvalidDocument("Document Dosen't Exists!")

    async def get_documents(
        self, name: KnowledgeBaseName
    ) -> list[DocumentId] | None:
        return await self.redis.json().get(f"knowledge_bases:{name}")

    async def validate_knowledge_base(
        self, name: KnowledgeBaseName
    ) -> list[DocumentId]:
        ids = await self.get_documents(f"{name}")
        if not isinstance(ids, list):
            raise InvalidKnowledgeBaseName("Knowledge Base Dosen't Exists!")
        return ids
