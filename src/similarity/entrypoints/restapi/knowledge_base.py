from fastapi import APIRouter, Depends, status
from similarity.container import Container
from similarity.domain.types import KnowledgeBaseName
from similarity.services.messagebus import MessageBus
from dependency_injector.wiring import Provide, inject


router = APIRouter(prefix="/knowledge_base")


from similarity.domain.commands import AddKnowledgeBase, RemoveKnowledgeBase


@router.post(path="", name="New KnowledgeBase", status_code=status.HTTP_201_CREATED)
@inject
async def new_knowledge_base(
    command: AddKnowledgeBase,
    bus: MessageBus = Depends(Provide[Container.knowledge_base_bus]),
) -> KnowledgeBaseName:
    knowledge_base = await bus.handle(command)
    return knowledge_base.name


@router.delete(
    path="", name="Remove KnowledgeBase", status_code=status.HTTP_202_ACCEPTED
)
@inject
async def remove_knowledge_base(
    command: RemoveKnowledgeBase,
    bus: MessageBus = Depends(Provide[Container.knowledge_base_bus]),
) -> KnowledgeBaseName:
    name = await bus.handle(command)
    return name
