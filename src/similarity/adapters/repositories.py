from similarity.adapters.protocols import DocumentProto, KnowledgeBaseProto
from similarity.domain.models import Document, KnowledgeBase
from similarity.domain.types import DocumentId, KnowledgeBaseName, LongStr


class KnowledgeBaseRepository:
    def __init__(self, adapter):
        self.adapter: KnowledgeBaseProto = adapter

    async def get(self, name: KnowledgeBaseName) -> list[DocumentId]:
        return await self.adapter.get_documents(name)

    async def add(self, knowledge_base: KnowledgeBase) -> KnowledgeBase:
        await self.adapter.add_knowledge_base(knowledge_base.name)
        return knowledge_base

    async def delete(self, name: KnowledgeBaseName) -> KnowledgeBaseName:
        await self.adapter.delete_knowledge_base(name)
        return name


class DocumentRepository:
    def __init__(self, adapter):
        self.adapter: DocumentProto = adapter

    async def get(self, content: LongStr, name: KnowledgeBaseName):
        return await self.adapter.get_similarity(query=content, name=name)

    async def add(self, document: Document, name: KnowledgeBaseName):
        await self.adapter.add_document(name=name, document=document)
        return document

    async def delete(self, id: DocumentId, name: KnowledgeBaseName):
        await self.adapter.delete_document(name=name, document_id=id)
        return id
