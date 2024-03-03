from similarity.domain.commands import AddDocument, RemoveDocument
from fastapi import Depends, status, Body, APIRouter, Path
from pydantic import BaseModel
from typing import Optional, Annotated
import uuid
from similarity.container import Container
from similarity.domain.types import DocumentId, KnowledgeBaseName, LongStr
from similarity.services.messagebus import MessageBus
from dependency_injector.wiring import Provide, inject


router = APIRouter(prefix="/knowledge_base")


class DocumentUseCase(BaseModel):
    id: Optional[DocumentId] = DocumentId(uuid.uuid4())
    content: LongStr


@router.post(
    path="/{name}/document", name="Add Document", status_code=status.HTTP_201_CREATED
)
@inject
async def new_document(
    uc: DocumentUseCase,
    name: str = Path(..., title="KnowledgeBase Name", regex="^[a-z0-9_]+$"),
    bus: MessageBus = Depends(Provide[Container.document_bus]),
) -> DocumentId:
    command = AddDocument(name=name, **uc.dict())
    document = await bus.handle(command)
    return document.id


@router.delete(
    path="/{name}/document",
    name="Remove Document",
    status_code=status.HTTP_202_ACCEPTED,
)
@inject
async def remove_document(
    id: Annotated[DocumentId, Body()],
    name: str = Path(..., title="KnowledgeBase Name", regex="^[a-z0-9_]+$"),
    bus: MessageBus = Depends(Provide[Container.document_bus]),
) -> DocumentId:
    command = RemoveDocument(name=name, id=id)
    id = await bus.handle(command)
    return id
