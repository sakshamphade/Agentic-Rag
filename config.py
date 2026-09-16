import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Embedding Model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Vector Database
VECTOR_DB_PATH = "vector_db"

# Data Folder
DATA_PATH = "data"

# Text Splitter
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retriever
TOP_K = 10

# Gemini Model
LLM_MODEL = "gemini-2.5-flash"