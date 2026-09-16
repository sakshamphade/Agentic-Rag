from config import DATA_PATH

from rag.pdf_loader import PDFLoader
from rag.splitter import TextSplitter
from rag.vectorstore import VectorStore

# Initialize loader
loader = PDFLoader(DATA_PATH)

# Load a single PDF
import os

pdf_path = os.path.join(DATA_PATH, "BEE notes.pdf")

documents = loader.load_pdf(pdf_path)

print("Pages:", len(documents))

# Split into chunks
splitter = TextSplitter()

chunks = splitter.split_documents(documents)

print("Chunks:", len(chunks))

# Store in Chroma
vectorstore = VectorStore()

vectorstore.add_documents(chunks)

print("PDF Added Successfully!")