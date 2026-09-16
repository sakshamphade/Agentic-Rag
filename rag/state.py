from typing import TypedDict, List

from langchain_core.documents import Document


class AgentState(TypedDict, total=False):

    question: str

    document_name: str

    decision: str

    documents: List[Document]

    web_results: str

    answer: str