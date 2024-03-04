import strawberry
from similarity.domain.types import KnowledgeBaseName, LongStr

from fastapi import Depends
from similarity.container import Container
from similarity.services.messagebus import MessageBus
from similarity import views
from dependency_injector.wiring import Provide, inject



@strawberry.type
class Document:
    id: str 
    content: str 

@inject
def get_uow(
        bus: MessageBus = Depends(Provide[Container.document_faiss_bus]),
    ):
        return bus.uow

@strawberry.type
class Query:

    @strawberry.field
    async def documents(self, content: LongStr,
    knowledge_base: KnowledgeBaseName,
    ) -> list[Document]:
        documents = await views.similarity(
            uow=get_uow(),
            content=content,
            name=knowledge_base
        )
        return [doc.to_schema(Document) for doc in documents]