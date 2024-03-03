from typing import Protocol
from .models import KnowledgeBase
from .types import KnowledgeBaseName


class KnowledgeBaseRepository(Protocol):
    async def add(self) -> KnowledgeBase:
        """
        Add a single knowledge base to your collection and returns the object
        """
    async def delete(self, name: KnowledgeBaseName) -> str:
        """
        Remove a single knowledge base based on name
        If knowledge base dosen't exist raise InvalidKnowledgeBase
        """