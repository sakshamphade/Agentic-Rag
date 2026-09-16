from rag.rag_chain import RAGChain

rag = RAGChain()

while True:

    question = input("\nAsk a Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    answer, docs = rag.ask(question)

    print("\nAnswer:\n")

    print(answer)

    print("\nSources:\n")

    for doc in docs:

        print(
            doc.metadata.get("source"),
            "Page",
            doc.metadata.get("page")
        )