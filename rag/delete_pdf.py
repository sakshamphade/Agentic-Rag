import os

from config import DATA_PATH

from rag.vectorstore import VectorStore


def delete_pdf(pdf_name):
    """
    Delete a PDF from the data folder
    and remove all of its embeddings
    from the Chroma vector database.
    """

    try:

        # ------------------------------------------
        # Create PDF Path
        # ------------------------------------------

        pdf_path = os.path.join(
            DATA_PATH,
            pdf_name
        )

        # ------------------------------------------
        # Check if PDF Exists
        # ------------------------------------------

        if not os.path.exists(pdf_path):

            return (
                False,
                f"'{pdf_name}' does not exist."
            )

        # ------------------------------------------
        # Delete PDF File
        # ------------------------------------------

        os.remove(pdf_path)

        print("\n===================================")
        print("PDF Deleted Successfully")
        print("File :", pdf_name)
        print("===================================")

        # ------------------------------------------
        # Delete Embeddings
        # ------------------------------------------

        vectorstore = VectorStore()

        db = vectorstore.get_vectorstore()

        db.delete(
            where={
                "source": pdf_name
            }
        )

        print("Embeddings Deleted Successfully")

        print("\n===================================")
        print("DELETE COMPLETED")
        print("===================================")

        return (
            True,
            f"'{pdf_name}' deleted successfully."
        )

    except Exception as e:

        print("\n===================================")
        print("DELETE FAILED")
        print(str(e))
        print("===================================")

        return (
            False,
            str(e)
        )