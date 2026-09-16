from langgraph.graph import StateGraph, END

from rag.state import AgentState

# Planner
from rag.planner import planner
from rag.router import router

# Nodes
from rag.tools.pdf_tool import retrieve_documents
from rag.agent import generate_answer
from rag.direct import direct_answer
from rag.calculator_node import calculator_node
from rag.time_node import time_node
from rag.web_search_node import web_search_node

# -----------------------------------
# Build Graph
# -----------------------------------

builder = StateGraph(AgentState)

# Planner
builder.add_node("planner", planner)

# PDF Retrieval
builder.add_node("pdf", retrieve_documents)

# PDF Answer
builder.add_node("generate", generate_answer)

# Calculator
builder.add_node("calculator", calculator_node)

# Time
builder.add_node("time", time_node)

# Direct Chat
builder.add_node("direct", direct_answer)

# Web Search
builder.add_node("web", web_search_node)

# -----------------------------------
# Entry Point
# -----------------------------------

builder.set_entry_point("planner")

# -----------------------------------
# Routing
# -----------------------------------

builder.add_conditional_edges(
    "planner",
    router,
    {
        "pdf": "pdf",
        "web": "web",
        "calculator": "calculator",
        "time": "time",
        "direct": "direct"
    }
)

# -----------------------------------
# Edges
# -----------------------------------

builder.add_edge("pdf", "generate")

builder.add_edge("generate", END)

builder.add_edge("web", END)

builder.add_edge("calculator", END)

builder.add_edge("time", END)

builder.add_edge("direct", END)

# -----------------------------------
# Compile
# -----------------------------------

graph = builder.compile()