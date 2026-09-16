from rag.vectorstore import VectorStore

db = VectorStore().get_vectorstore()

docs = db.similarity_search(
    "transformer",
    k=5,
    filter={"source": "BEE notes.pdf"}
)

print("Retrieved:", len(docs))

for doc in docs:
    print(doc.metadata)
    print(doc.page_content[:300])
    print("=" * 50)