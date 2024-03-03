from typing import Protocol
from similarity.domain.models import Document

from similarity.domain.types import DocumentId, KnowledgeBaseName


class KnowledgeBaseProto(Protocol):
    async def add_knowledge_base(self, name: KnowledgeBaseName): ...
    async def delete_knowledge_base(self, name: KnowledgeBaseName): ...


class DocumentProto(Protocol):
    async def add_document(self, name: KnowledgeBaseName, document: Document): ...
    async def delete_document(self, name: KnowledgeBaseName, id: DocumentId): ...
