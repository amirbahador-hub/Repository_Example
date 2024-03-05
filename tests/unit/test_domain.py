from dataclasses import dataclass
from similarity.domain import models
from similarity.domain import commands
from pydantic import ValidationError
import pytest
import uuid


class TestKnowledgeBase:

    def test_getting_new_instance(self):
        command = commands.AddKnowledgeBase(name="books")
        knowledge_base = models.KnowledgeBase.new_instance(command)
        assert knowledge_base.name == command.name
        assert isinstance(knowledge_base, models.KnowledgeBase)

    def test_name_validation(self):
        with pytest.raises(ValidationError):
            commands.AddKnowledgeBase(name="Books")
        with pytest.raises(ValidationError):
            commands.AddKnowledgeBase(name="b@ooks")
        with pytest.raises(ValidationError):
            commands.AddKnowledgeBase(name="book s")

    def test_for_remove_knowledge_base_unhappy_path(self): ...


class TestDocument:

    def test_convert_schema(self):
        @dataclass
        class Schema:
            id: str
            content: str

        document = models.Document(id=uuid.uuid4(), content="SS")
        new_schema = document.to_schema(Schema)
        assert new_schema.id == document.id
        assert isinstance(new_schema, Schema)

    def test_getting_new_instance(self):
        command = commands.AddDocument(name="books", content="SS", id=uuid.uuid4())
        document = models.Document.new_instance(command)
        assert document.id == command.id
        assert isinstance(document, models.Document)
