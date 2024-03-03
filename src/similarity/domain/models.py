from __future__ import annotations
from datetime import date
from .commands import AddKnowledgeBase
from .types import KnowledgeBaseName, DocumentId, LongStr


class KnowledgeBase:
    def __init__(self, name: KnowledgeBaseName, documents: list[Document] = [], eta: date | None = None):
        self.name = name
        self.documents = documents
        self.eta = eta
        self.events = []  # type: List[events.Event]

    def __repr__(self):
        return f"<KnowledgeBase {self.name}>"

    def __eq__(self, other):
        if not isinstance(other, KnowledgeBase):
            return False
        return other.name == self.name

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __hash__(self):
        return hash(self.name)

    @staticmethod
    def new_instance(command: AddKnowledgeBase) -> 'KnowledgeBase':
        return KnowledgeBase(**command.dict())

class Document:
    def __init__(self, id: DocumentId, content: LongStr):
        self.id = id 
        self.content = content
        self.events = []  # type: List[events.Event]

    def __repr__(self):
        return f"<Document {self.id}>"

    def __eq__(self, other):
        if not isinstance(other, Document):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)
