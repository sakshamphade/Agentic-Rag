from rag.llm import GeminiLLM
from rag.memory import memory

# Initialize Gemini
llm = GeminiLLM().get_llm()


def direct_answer(state):
    """
    Answer general questions without searching documents.
    Uses conversation memory.
    """

    # -----------------------------------------
    # Build Conversation History
    # -----------------------------------------

    history = ""

    for message in memory.messages:
        history += f"{message.type.upper()}: {message.content}\n"

    # -----------------------------------------
    # Prompt
    # -----------------------------------------

    prompt = f"""
You are an intelligent AI assistant.

You are having a conversation with the user.

Below is the previous conversation.

==============================
PREVIOUS CONVERSATION
==============================

{history}

==============================
CURRENT QUESTION
==============================

{state["question"]}

==============================
INSTRUCTIONS
==============================

1. Use the previous conversation whenever needed.
2. Answer naturally and conversationally.
3. If the current question refers to previous messages
   (such as "it", "that", "those", "he", "she"),
   use the conversation history.
4. Be helpful, accurate, and concise.

==============================
FINAL ANSWER
==============================
"""

    # -----------------------------------------
    # Stream Response from Gemini
    # -----------------------------------------

    answer = ""

    for chunk in llm.stream(prompt):

        if chunk.content:

            answer += chunk.content

    # -----------------------------------------
    # Save Conversation
    # -----------------------------------------

    memory.add_user_message(state["question"])
    memory.add_ai_message(answer)

    # -----------------------------------------
    # Return
    # -----------------------------------------

    return {
        "answer": answer
    }