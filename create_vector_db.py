import shutil
import os

from config import DATA_PATH, VECTOR_DB_PATH
from rag.pdf_loader import PDFLoader
from rag.splitter import TextSplitter
from rag.vectorstore import VectorStore

# Delete old vector database if it exists
if os.path.exists(VECTOR_DB_PATH):
    print("Deleting old vector database...")
    shutil.rmtree(VECTOR_DB_PATH)

# Load PDFs
loader = PDFLoader(DATA_PATH)
documents = loader.load_pdfs()

print(f"\nLoaded {len(documents)} pages")

# Split into chunks
splitter = TextSplitter()
chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# Create vector database
db = VectorStore()
db.add_documents(chunks)

print("\n✅ Vector Database Created Successfully!")