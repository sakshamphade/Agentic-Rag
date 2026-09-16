from rag.graph import graph

state = {

    "question": "Summarize transformer.",

    "document_name": "BEE notes.pdf"
}

result = graph.invoke(state)

print("\nDecision :", result["decision"])

print("\nAnswer :\n")

print(result["answer"])