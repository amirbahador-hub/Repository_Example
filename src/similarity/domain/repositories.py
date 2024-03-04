from typing import Protocol
from .models import KnowledgeBase, Document
from .types import DocumentId, KnowledgeBaseName


class KnowledgeBaseRepository(Protocol):
    async def get(self, name: KnowledgeBaseName) -> list[DocumentId]:
        """
        retrive all of the documents for the given knowledge_base name
        """
    async def add(self) -> KnowledgeBase:
        """
        Add a single knowledge base to your collection and returns the object
        """

    async def delete(self, name: KnowledgeBaseName) -> KnowledgeBaseName:
        """
        Remove a single knowledge base based on name
        If knowledge base dosen't exist raise InvalidKnowledgeBase
        """


class DocumentRepository(Protocol):
    async def add(self) -> Document:
        """
        Add a single document to your knowledge_base
        """

    async def delete(self, id: DocumentId) -> DocumentId:
        """
        Remove a single document based on id
        If document dosen't exist raise InvalidDocument
        """
