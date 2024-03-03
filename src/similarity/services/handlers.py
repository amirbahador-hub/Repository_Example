# pylint: disable=unused-argument
from __future__ import annotations
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from similarity.domain import commands, events, models
from dependency_injector.wiring import inject

if TYPE_CHECKING:
    from . import unit_of_work


async def add_knowledge_base(
    cmd: commands.AddKnowledgeBase,
    uow: unit_of_work.AbstractUnitOfWork,
):
    knowledge_base = models.KnowledgeBase.new_instance(cmd)
    return await uow.repository.add(knowledge_base)

async def remove_knowledge_base(
    cmd: commands.RemoveKnowledgeBase,
    uow: unit_of_work.AbstractUnitOfWork,
):
    return await uow.repository.delete(cmd.name)


EVENT_HANDLERS = {
    # events.Allocated: [publish_allocated_event, add_allocation_to_read_model],
    # events.Deallocated: [remove_allocation_from_read_model, reallocate],
    # events.OutOfStock: [send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    # commands.Allocate: allocate,
    commands.AddKnowledgeBase: add_knowledge_base,
    commands.RemoveKnowledgeBase: remove_knowledge_base,
    # commands.ChangeBatchQuantity: change_batch_quantity,
}  # type: Dict[Type[commands.Command], Callable]
