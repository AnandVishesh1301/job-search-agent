from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import fetch_node, parse_node, clean_node, extract_node

def build_graph():
    g = StateGraph(AgentState)
    g.add_node("fetch", fetch_node)
    g.add_node("parse", parse_node)
    g.add_node("clean", clean_node)
    g.add_node("extract", extract_node)

    g.set_entry_point("fetch")
    g.add_edge("fetch", "parse")
    g.add_edge("parse", "clean")
    g.add_edge("clean", "extract")
    g.add_edge("extract", END)

    return g.compile()
