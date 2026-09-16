from rag.retriever import Retriever
from rag.llm import GeminiLLM


class RAGChain:

    def __init__(self):

        self.retriever = Retriever()

        self.llm = GeminiLLM().get_llm()

    def ask(self, question, document_name=None):

        docs = self.retriever.retrieve(question, document_name)

        # Debug: Print retrieved documents
        print("\n===== Retrieved Documents =====")

        for i, doc in enumerate(docs, start=1):
            print(f"\nDocument {i}")
            print("Source:", doc.metadata.get("source"))
            print("Page:", doc.metadata.get("page"))
            print(doc.page_content[:300])

        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        prompt = f"""
You are an AI assistant.

Answer ONLY using the context below.

If the answer is not available, reply exactly:

"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.llm.invoke(prompt)

        return response.content, docs