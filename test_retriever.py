from rag.retriever import Retriever

retriever = Retriever()

question = input("Ask a Question: ")

documents = retriever.retrieve(question)

print("\nRetrieved Documents\n")

for i, doc in enumerate(documents, start=1):

    print("=" * 60)

    print(f"Result {i}")

    print("Source :", doc.metadata.get("source"))

    print("Page   :", doc.metadata.get("page"))

    print("\nContent:\n")

    print(doc.page_content[:500])