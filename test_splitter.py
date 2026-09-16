from rag.pdf_loader import PDFLoader
from rag.splitter import TextSplitter
from config import DATA_PATH

loader = PDFLoader(DATA_PATH)

documents = loader.load_pdfs()

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print("=" * 50)
print(f"Total Chunks: {len(chunks)}")
print("=" * 50)

for chunk in chunks[:5]:

    print()

    print(chunk["source"])
    print("Page:", chunk["page"])

    print(chunk["text"][:250])

    print("-" * 40)