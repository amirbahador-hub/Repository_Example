import uuid
from similarity.services import messagebus
from similarity.services import handlers
from similarity.domain import commands
import pytest

from similarity.services.unit_of_work import (
    DocumentPersistenceUnitOfWork,
    KnowledgeBasePersistenceUnitOfWork,
)


class FakeAdapter:
    def __init__(self):
        self.db = dict()

    async def get_documents(self, name):
        return self.db[name]

    async def get_knowledge_bases(self):
        return list(self.db.keys())

    async def add_knowledge_base(self, name):
        self.db.update({name: []})
        return name

    async def delete_knowledge_base(self, name):
        del self.db[name]
        return name

    async def add_document(self, document, name):
        knowledge_base = self.db.get(name) or []
        self.db.update({name: knowledge_base + [document.id]})

    async def delete_document(self, document_id, name):
        knowledge_base = self.db[name]
        knowledge_base.remove(document_id)
        self.db.update({name: knowledge_base})


def bootstrap_message_bus(UnitOfWork, adapter):
    return messagebus.MessageBus(
        uow=UnitOfWork(adapter),
        event_handlers=handlers.EVENT_HANDLERS,
        command_handlers=handlers.COMMAND_HANDLERS,
    )


class TestKnowledgeBase:
    @pytest.mark.asyncio
    async def test_for_new_knowledge_base(self):
        db = FakeAdapter()
        bus = bootstrap_message_bus(KnowledgeBasePersistenceUnitOfWork, db)
        await bus.handle(commands.AddKnowledgeBase(name="book"))
        assert "book" in await db.get_knowledge_bases()

    @pytest.mark.asyncio
    async def test_for_remove_knowledge_base_happy_path(self):
        db = FakeAdapter()
        bus = bootstrap_message_bus(KnowledgeBasePersistenceUnitOfWork, db)
        await bus.handle(commands.AddKnowledgeBase(name="book"))
        assert "book" in await db.get_knowledge_bases()
        await bus.handle(commands.RemoveKnowledgeBase(name="book"))
        assert "book" not in await db.get_knowledge_bases()

    @pytest.mark.asyncio
    async def test_for_remove_knowledge_base_unhappy_path(self):
        bus = bootstrap_message_bus(KnowledgeBasePersistenceUnitOfWork, FakeAdapter())
        with pytest.raises(Exception):
            await bus.handle(commands.RemoveKnowledgeBase(name="family"))


class TestDocument:

    @pytest.mark.asyncio
    async def test_for_new_document_happy_path(self):
        db = FakeAdapter()
        bus = bootstrap_message_bus(DocumentPersistenceUnitOfWork, db)
        _id = uuid.uuid4()
        await bus.handle(
            commands.AddDocument(id=_id, content="random string", name="book")
        )
        uow = KnowledgeBasePersistenceUnitOfWork(db)
        async with uow:
            assert _id in await uow.repository.get("book")

    @pytest.mark.asyncio
    async def test_for_remove_document_happy_path(self):
        db = FakeAdapter()
        bus = bootstrap_message_bus(DocumentPersistenceUnitOfWork, db)
        _id = uuid.uuid4()
        await bus.handle(
            commands.AddDocument(id=_id, content="random string", name="book")
        )
        await bus.handle(commands.RemoveDocument(id=_id, name="book"))
        uow = KnowledgeBasePersistenceUnitOfWork(db)
        async with uow:
            assert _id not in await uow.repository.get("book")

    @pytest.mark.asyncio
    async def test_for_remove_document_unhappy_path(self):
        db = FakeAdapter()
        bus = bootstrap_message_bus(DocumentPersistenceUnitOfWork, db)
        _id = uuid.uuid4()
        with pytest.raises(Exception):
            await bus.handle(commands.RemoveDocument(id=_id, name="book"))
