from config import DATA_PATH

from rag.pdf_loader import PDFLoader
from rag.splitter import TextSplitter
from rag.vectorstore import VectorStore


loader = PDFLoader(DATA_PATH)

documents = loader.load_pdfs()

print(f"Loaded {len(documents)} pages")

splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

db = VectorStore()

db.add_documents(chunks)

print("Vector Database Created Successfully!")