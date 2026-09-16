from rag.pdf_loader import PDFLoader
from config import DATA_PATH

loader = PDFLoader(DATA_PATH)

documents = loader.load_pdfs()

print("=" * 50)
print(f"Documents Loaded: {len(documents)}")
print("=" * 50)

for doc in documents[:3]:
    print(doc)