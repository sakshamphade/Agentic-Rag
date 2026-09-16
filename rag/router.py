def router(state):

    decision = state["decision"]

    if decision == "PDF":
        return "pdf"

    elif decision == "WEB":
        return "web"

    elif decision == "CALCULATOR":
        return "calculator"

    elif decision == "TIME":
        return "time"

    return "direct"