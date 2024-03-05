from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from similarity.domain import models
from similarity.domain.types import DocumentId, KnowledgeBaseName


class FaissOrm:
    def __init__(self):
        self.db = FAISS.from_documents([Document("init")], self.get_model(), ids=["init"])

    async def _ingest(self, *, sentences: list[str], knowledge_base_name: str, ids: list[str]) -> None:
        documents = [Document(page_content=sentence, metadata=dict(id=id, collection=knowledge_base_name)) for sentence, id in zip(sentences, ids)]
        await self.db.aadd_documents(documents, ids=ids)

    async def get_similarity(self, query: str, name: str) -> list[models.Document]:
        docs = await self.db.asimilarity_search_with_score(query, filter=dict(collection=name))
        return [models.Document(id=doc.metadata["id"], content=doc.page_content) for doc, _ in docs]

    @staticmethod
    def get_model() -> FAISS:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2") # TODO: maybe we should preload this!

    async def add_document(self, document: models.Document, name: KnowledgeBaseName):
        await self._ingest(sentences=[document.content], knowledge_base_name=name, ids=[str(document.id)])

    async def delete_document(self, document_id: DocumentId, name: KnowledgeBaseName):
        try:
            self.db.delete([str(document_id)])
        except ValueError:
            #raise exceptions.InvalidDocument(f"{document_id} dosen't exsist!!") 
            print(f"{document_id} dosen't exsist!!")
