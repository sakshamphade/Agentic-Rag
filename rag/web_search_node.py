from ddgs import DDGS

from rag.llm import GeminiLLM
from rag.memory import memory

llm = GeminiLLM().get_llm()


def web_search_node(state):

    question = state["question"]

    print("\n========== WEB NODE START ==========")
    print("Question:", question)

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    question,
                    max_results=5
                )
            )

        print("Results Found:", len(results))

    except Exception as e:

        print("Search Error:", e)

        return {
            "decision": "WEB",
            "answer": f"Search Error: {e}",
            "web_results": ""
        }

    if not results:

        return {
            "decision": "WEB",
            "answer": "No web results found.",
            "web_results": ""
        }

    web_context = ""

    for i, result in enumerate(results, start=1):

        title = result.get("title", "")
        body = result.get("body", "")
        href = result.get("href", "")

        web_context += f"""
Result {i}

Title:
{title}

Content:
{body}

URL:
{href}

----------------------------------------
"""

    prompt = f"""
You are an AI assistant.

Answer the user's question using the search results below.

Search Results:

{web_context}

Question:

{question}

Answer in a clear and concise way.
"""

    response = llm.invoke(prompt)

    memory.add_user_message(question)
    memory.add_ai_message(response.content)

    return {
        "decision": "WEB",
        "answer": response.content,
        "web_results": web_context
    }