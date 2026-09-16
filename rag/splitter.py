from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class TextSplitter:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len
        )

    def split_documents(self, documents):

        chunks = self.splitter.split_documents(documents)

        print(f"Created {len(chunks)} chunks")

        return chunks