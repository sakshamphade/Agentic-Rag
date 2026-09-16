import os

from config import DATA_PATH


def get_pdf_files():
    """
    Return all PDF files present in the data folder.
    """

    pdf_files = [
        file
        for file in os.listdir(DATA_PATH)
        if file.endswith(".pdf")
    ]

    pdf_files.sort()

    return pdf_files