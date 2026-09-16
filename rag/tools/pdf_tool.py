from rag.retriever import Retriever

retriever = Retriever()


def retrieve_documents(state):
    """
    Retrieve relevant documents from ChromaDB.
    """

    docs = retriever.retrieve(
        state["question"],
        state.get("document_name")
    )

    print("\n========== RETRIEVED DOCUMENTS ==========")

    if not docs:
        print("No documents retrieved!")

    for i, doc in enumerate(docs, start=1):

        print(f"\nDocument {i}")

        print(
            "Source:",
            doc.metadata.get("source")
        )

        print(
            "Page:",
            doc.metadata.get("page")
        )

        print(doc.page_content[:200])

    return {
        "documents": docs
    }