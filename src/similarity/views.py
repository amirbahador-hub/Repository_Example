from similarity.domain.models import Document
from similarity.domain.types import KnowledgeBaseName, LongStr
from similarity.services import unit_of_work


async def similarity(content: LongStr, name: KnowledgeBaseName, uow: unit_of_work.DocumentPersistenceUnitOfWork) -> list[Document]:
    async with uow:
        results = await uow.repository.get(
            content=content, name=name
        )
    return results
