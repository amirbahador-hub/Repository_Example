from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from similarity.domain import models, exceptions
from similarity.domain.types import DocumentId, KnowledgeBaseName



class FaissOrm:
    def __init__(self):
        self.db = None

    async def _ingest(self, *, sentences: list[str], knowledge_base_name: str, ids: list[str]) -> None:
        documents = [Document(page_content=sentence, metadata=dict(id=id, collection=knowledge_base_name)) for sentence, id in zip(sentences, ids)]
        if not self.db:
            self.db = await FAISS.afrom_documents(documents, self.get_model(), ids=ids)
        else:
            await self.db.aadd_documents(documents)

    def get_similarity(self, query: str, knowledge_base_name: str) -> Document:
        return self.db.similarity_search_with_score(query, filter=dict(collection=knowledge_base_name))

    @staticmethod
    def get_model() -> FAISS:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L12-v2") # TODO: maybe we should preload this!

    async def preload(self):
        self.db = FAISS.load_local("faiss_index", self.get_model())
        # await self._ingest(sentences=["Test Faiss"], knowledge_base_name="initial", ids=["test_id"])
        # await self.delete_document(document_id="test_id", name="initial")

    async def add_document(self, document: models.Document, name: KnowledgeBaseName):
        await self._ingest(sentences=[document.content], knowledge_base_name=name, ids=[str(document.id)])

    async def delete_document(self, document_id: DocumentId, name: KnowledgeBaseName):
        try:
            self.db.delete([str(document_id)])
        except ValueError:
            #raise exceptions.InvalidDocument(f"{document_id} dosen't exsist!!") 
            print(f"{document_id} dosen't exsist!!")