from rag.llm import GeminiLLM

# Initialize Gemini
llm = GeminiLLM().get_llm()


def planner(state):
    """
    Decide which tool should answer the user's question.
    """

    question = state["question"]

    prompt = f"""
You are an AI Planner.

Your job is to decide which tool should answer the user's question.

Return ONLY ONE WORD.

Possible outputs:

PDF
WEB
CALCULATOR
TIME
DIRECT

------------------------------------------------------------
1. PDF
------------------------------------------------------------

Choose PDF when the answer should come from the uploaded PDF documents.

Examples:

Explain transformer

Summarize BEE notes

What is Ohm's law?

Explain Python loops

Define Machine Learning

Return:

PDF

------------------------------------------------------------
2. WEB
------------------------------------------------------------

Choose WEB when the question requires current internet knowledge,
latest information, famous people, places, companies, news,
or anything NOT expected inside uploaded PDFs.

Examples:

Who is Elon Musk?

Latest IPL winner

Current Prime Minister of India

What is ChatGPT?

Latest AI news

Weather in Mumbai

Return:

WEB

------------------------------------------------------------
3. CALCULATOR
------------------------------------------------------------

Choose CALCULATOR for mathematical calculations.

Examples:

2+2

100/5

sqrt(144)

25*78

5^3

(10+20)*5

Return:

CALCULATOR

------------------------------------------------------------
4. TIME
------------------------------------------------------------

Choose TIME when the user asks the current time or today's date.

Examples:

What time is it?

Current time

Today's date

Current date

Return:

TIME

------------------------------------------------------------
5. DIRECT
------------------------------------------------------------

Choose DIRECT for normal conversation.

Examples:

Hello

Hi

Who are you?

Tell me a joke

Thank you

Good morning

Return:

DIRECT

------------------------------------------------------------

Question:

{question}

Return ONLY ONE WORD.
"""

    response = llm.invoke(prompt)

    decision = response.content.strip().upper()

    print("\n==============================")
    print("Planner Question :", question)
    print("Planner Decision :", decision)
    print("==============================")

    # Safety check
    if decision not in [
        "PDF",
        "WEB",
        "CALCULATOR",
        "TIME",
        "DIRECT"
    ]:
        decision = "DIRECT"

    return {
        "decision": decision
    }