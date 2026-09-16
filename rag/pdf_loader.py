from pathlib import Path

from langchain_core.documents import Document

from pypdf import PdfReader


class PDFLoader:

    def __init__(self, data_path):

        self.data_path = Path(data_path)

    # -----------------------------------------
    # Load ALL PDFs from data folder
    # -----------------------------------------

    def load_pdfs(self):

        documents = []

        pdf_files = list(
            self.data_path.glob("*.pdf")
        )

        if not pdf_files:

            print("No PDF files found.")

            return documents

        for pdf in pdf_files:

            print(f"Reading: {pdf.name}")

            reader = PdfReader(pdf)

            for page_number, page in enumerate(reader.pages):

                text = page.extract_text()

                if text and text.strip():

                    documents.append(

                        Document(

                            page_content=text,

                            metadata={
                                "source": pdf.name,
                                "page": page_number + 1
                            }

                        )

                    )

        return documents

    # -----------------------------------------
    # NEW
    # Load ONE uploaded PDF
    # -----------------------------------------

    def load_pdf(self, pdf_path):

        documents = []

        pdf_path = Path(pdf_path)

        reader = PdfReader(pdf_path)

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if text and text.strip():

                documents.append(

                    Document(

                        page_content=text,

                        metadata={
                            "source": pdf_path.name,
                            "page": page_number + 1
                        }

                    )

                )

        return documents