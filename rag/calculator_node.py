import math


def calculator_node(state):

    question = state["question"].strip().lower()

    try:

        # sqrt()
        if question.startswith("sqrt(") and question.endswith(")"):

            number = float(question[5:-1])

            answer = str(math.sqrt(number))

        else:

            answer = str(eval(question))

    except Exception:

        answer = "Invalid mathematical expression."

    return {
        "answer": answer
    }