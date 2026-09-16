from rag.vectorstore import VectorStore
from config import TOP_K


class Retriever:

    def __init__(self):

        self.vectorstore = VectorStore().get_vectorstore()

    def retrieve(self, question, document_name=None):

        # Search inside selected PDF
        if document_name:

            results = self.vectorstore.similarity_search_with_score(
                question,
                k=TOP_K,
                filter={
                    "source": document_name
                }
            )

        else:

            results = self.vectorstore.similarity_search_with_score(
                question,
                k=TOP_K
            )

        documents = []

        for doc, score in results:

            # Convert distance into similarity percentage
            similarity = max(
                0,
                min(
                    100,
                    round((1 - score) * 100)
                )
            )

            doc.metadata["similarity"] = similarity

            documents.append(doc)

        return documents