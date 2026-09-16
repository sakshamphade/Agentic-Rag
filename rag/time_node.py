from rag.tools.datetime_tool import current_datetime


def time_node(state):

    return {

        "answer": current_datetime()

    }