from langchain_google_genai import ChatGoogleGenerativeAI
import config


class GeminiLLM:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0.3
        )

    def get_llm(self):
        return self.llm