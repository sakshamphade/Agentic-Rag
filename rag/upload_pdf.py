import os
import shutil

from config import DATA_PATH

from rag.pdf_loader import PDFLoader
from rag.splitter import TextSplitter
from rag.vectorstore import VectorStore


def upload_pdf(uploaded_file, progress_bar=None, status=None):
    """
    Upload a PDF, generate embeddings,
    and store them in the vector database.
    """

    try:

        # -----------------------------------------
        # Step 1 : Saving PDF
        # -----------------------------------------

        if status:
            status.text("📥 Saving PDF...")

        pdf_path = os.path.join(
            DATA_PATH,
            uploaded_file.name
        )

        # -----------------------------------------
        # Duplicate File Check
        # -----------------------------------------

        if os.path.exists(pdf_path):

            return (
                False,
                f"'{uploaded_file.name}' has already been uploaded."
            )

        with open(pdf_path, "wb") as file:

            shutil.copyfileobj(
                uploaded_file,
                file
            )

        if progress_bar:
            progress_bar.progress(20)

        print("\n===================================")
        print("PDF Saved Successfully")
        print("File :", uploaded_file.name)
        print("Path :", pdf_path)
        print("===================================")

        # -----------------------------------------
        # Step 2 : Load PDF
        # -----------------------------------------

        if status:
            status.text("📖 Reading PDF...")

        loader = PDFLoader(DATA_PATH)

        documents = loader.load_pdf(
            pdf_path
        )

        if progress_bar:
            progress_bar.progress(40)

        print(f"Pages Loaded : {len(documents)}")

        # -----------------------------------------
        # Step 3 : Split PDF
        # -----------------------------------------

        if status:
            status.text("✂ Splitting into chunks...")

        splitter = TextSplitter()

        chunks = splitter.split_documents(
            documents
        )

        if progress_bar:
            progress_bar.progress(60)

        print(f"Chunks Created : {len(chunks)}")

        # -----------------------------------------
        # Step 4 : Store Embeddings
        # -----------------------------------------

        if status:
            status.text("🧠 Generating embeddings...")

        vectorstore = VectorStore()

        vectorstore.add_documents(
            chunks
        )

        if progress_bar:
            progress_bar.progress(90)

        print("Embeddings Stored Successfully")

        # -----------------------------------------
        # Step 5 : Finish
        # -----------------------------------------

        if status:
            status.text("✅ Upload Completed")

        if progress_bar:
            progress_bar.progress(100)

        print("\n===================================")
        print("UPLOAD COMPLETED")
        print("===================================")

        return (
            True,
            f"'{uploaded_file.name}' uploaded successfully."
        )

    except Exception as e:

        print("\n===================================")
        print("UPLOAD FAILED")
        print(str(e))
        print("===================================")

        return (
            False,
            str(e)
        )