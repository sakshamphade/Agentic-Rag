from langchain_huggingface import HuggingFaceEmbeddings
from config import EMBEDDING_MODEL

class EmbeddingModel:

    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

    def get_embedding(self):
        return self.embedding