from similarity.domain.commands import AddDocument, RemoveDocument
from fastapi import Depends, status, Body, APIRouter, Path
from pydantic import BaseModel, Field
from typing import Optional, Annotated
import uuid
from similarity.container import APIContainer as Container
from similarity import views
from similarity.domain.types import DocumentId, LongStr
from similarity.services.messagebus import MessageBus
from similarity.adapters.redis_publisher import publish
from dependency_injector.wiring import Provide, inject


router = APIRouter(prefix="/knowledge_base")


class DocumentUseCase(BaseModel):
    # id: Optional[DocumentId] = Depends(DocumentId(uuid.uuid4()))
    id: DocumentId = Field(
        default_factory=uuid.uuid4,
    )
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
    await publish(
        "document.add", command
    )  # TODO: we can use gather as well if we don't care about saving into redis first
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
    await bus.handle(command)
    await publish("document.remove", command)
    return id


@router.get(
    path="/{name}/document/",
    name="Get Similar Document",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_documents(
    name: str = Path(..., title="KnowledgeBase Name", regex="^[a-z0-9_]+$"),
    bus: MessageBus = Depends(Provide[Container.document_bus]),
    q: str | None = None,
) -> list[DocumentUseCase]:
    documents = await views.similarity(uow=bus.uow, content=q, name=name)
    return [doc.to_schema(DocumentUseCase) for doc in documents]
