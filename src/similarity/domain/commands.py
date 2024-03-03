# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional
from pydantic import BaseModel, validator

from similarity.domain.types import DocumentId, KnowledgeBaseName, LongStr
from similarity.utils import clean_name


class Command(BaseModel):
    pass


class AddKnowledgeBase(Command):
    name: KnowledgeBaseName
    eta: Optional[date] = None

    @validator("name")
    def url_friendly(cls, value, *, values, **kwargs):
        return clean_name(value)


class RemoveKnowledgeBase(Command):
    name: KnowledgeBaseName


class AddDocument(Command):
    id: DocumentId
    content: LongStr
    name: KnowledgeBaseName


class RemoveDocument(Command):
    id: DocumentId
    name: KnowledgeBaseName
