from langchain_chroma import Chroma

from config import VECTOR_DB_PATH

from rag.embedding import EmbeddingModel


class VectorStore:

    def __init__(self):

        embedding = EmbeddingModel().get_embedding()

        self.db = Chroma(

            persist_directory=VECTOR_DB_PATH,

            embedding_function=embedding
        )

    def add_documents(self, documents):

        self.db.add_documents(documents)

    def similarity_search(self, query, k=5):

        return self.db.similarity_search(

            query,

            k=k
        )

    def similarity_search_with_score(self, query, k=5):

        return self.db.similarity_search_with_score(

            query,

            k=k
        )

    def get_vectorstore(self):

        return self.db