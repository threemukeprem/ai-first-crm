from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.services.interaction_ai_service import analyze_interaction


class InteractionState(TypedDict):
    notes: str
    summary: str
    sentiment: str
    suggested_follow_up: str
    provider: str


def analyze_node(state: InteractionState):
    result = analyze_interaction(state["notes"])

    return {
        "notes": state["notes"],
        "summary": result.summary,
        "sentiment": result.sentiment,
        "suggested_follow_up": result.suggested_follow_up,
        "provider": result.provider,
    }


builder = StateGraph(InteractionState)

builder.add_node("analyze", analyze_node)

builder.set_entry_point("analyze")

builder.add_edge("analyze", END)

interaction_graph = builder.compile()


def analyze_with_graph(notes: str):
    state = interaction_graph.invoke(
        {
            "notes": notes,
        }
    )

    return state