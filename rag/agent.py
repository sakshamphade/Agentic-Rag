from rag.llm import GeminiLLM
from rag.memory import memory

# Initialize Gemini
llm = GeminiLLM().get_llm()


def generate_answer(state):
    """
    Generate answer using retrieved documents
    and conversation memory.
    """

    documents = state.get("documents", [])

    # No documents found
    if not documents:
        return {
            "answer": "I couldn't find any relevant information in the uploaded documents."
        }

    # Create document context
    context = "\n\n".join(
        [
            f"Source: {doc.metadata.get('source')} | Page: {doc.metadata.get('page')}\n{doc.page_content}"
            for doc in documents
        ]
    )

    # Build conversation history
    history = ""

    for message in memory.messages:
        history += f"{message.type.upper()}: {message.content}\n"

    # Prompt
    prompt = f"""
You are an intelligent AI Research Assistant.

You have access to:

1. Previous conversation history.
2. Retrieved document context.

Use BOTH whenever necessary.

==============================
PREVIOUS CONVERSATION
==============================

{history}

==============================
DOCUMENT CONTEXT
==============================

{context}

==============================
CURRENT QUESTION
==============================

{state["question"]}

==============================
INSTRUCTIONS
==============================

1. Read the conversation history.
2. Read the document context carefully.
3. Answer ONLY using the provided context.
4. If the current question refers to previous questions
   (for example: "its", "that", "those", "it"),
   use the conversation history.
5. Never make up information.
6. If the answer does not exist in the document context,
   reply exactly:

"I don't know based on the uploaded documents."

==============================
FINAL ANSWER
==============================
"""

    # Debug (optional)
    print("\n========== CONTEXT SENT TO GEMINI ==========\n")
    print(context[:1500])

    # Generate answer
    response = llm.invoke(prompt)

    # Save conversation in memory
    memory.add_user_message(state["question"])
    memory.add_ai_message(response.content)

    return {
        "answer": response.content
    }