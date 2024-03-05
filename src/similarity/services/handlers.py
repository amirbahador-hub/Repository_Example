# pylint: disable=unused-argument
from __future__ import annotations
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from similarity import adapters
from similarity.domain import commands, events, models
import asyncio

if TYPE_CHECKING:
    from . import unit_of_work


async def add_knowledge_base(
    cmd: commands.AddKnowledgeBase,
    uow: unit_of_work.AbstractUnitOfWork,
):
    async with uow:
        knowledge_base = models.KnowledgeBase.new_instance(cmd)
        return await uow.repository.add(knowledge_base)


async def remove_knowledge_base(
    cmd: commands.RemoveKnowledgeBase,
    uow: unit_of_work.AbstractUnitOfWork,
):
    async with uow:
        document_ids = await uow.repository.get(cmd.name)
        name = await uow.repository.delete(cmd.name)
        tasks = [
            adapters.redis_publisher.publish(
                "document.remove", {"id": id, "name": name}
            )
            for id in document_ids
        ]
        await asyncio.gather(*tasks)
        return name


async def add_document(
    cmd: commands.AddDocument,
    uow: unit_of_work.AbstractUnitOfWork,
):
    async with uow:
        document = models.Document.new_instance(cmd)
        return await uow.repository.add(document, name=cmd.name)


async def remove_document(
    cmd: commands.RemoveDocument,
    uow: unit_of_work.AbstractUnitOfWork,
):
    async with uow:
        return await uow.repository.delete(id=cmd.id, name=cmd.name)


EVENT_HANDLERS = {
    # events.Allocated: [publish_allocated_event, add_allocation_to_read_model],
    # events.Deallocated: [remove_allocation_from_read_model, reallocate],
    # events.OutOfStock: [send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddKnowledgeBase: add_knowledge_base,
    commands.RemoveKnowledgeBase: remove_knowledge_base,
    commands.AddDocument: add_document,
    commands.RemoveDocument: remove_document,
}  # type: Dict[Type[commands.Command], Callable]
