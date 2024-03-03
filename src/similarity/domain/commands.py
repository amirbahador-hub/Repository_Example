# pylint: disable=too-few-public-methods
from datetime import date
from typing import Optional
from pydantic import BaseModel, validator
from fastapi import Depends
from dataclasses import dataclass

from similarity.domain.types import KnowledgeBaseName
from similarity.utils import clean_name


class Command(BaseModel):
    pass


@dataclass
class AddKnowledgeBase(Command):
    name: KnowledgeBaseName
    eta: Optional[date] = None


    @validator("name")
    def url_friendly(cls, value, *, values, **kwargs):
        return clean_name(value)

@dataclass
class RemoveKnowledgeBase(Command):
    name: KnowledgeBaseName

