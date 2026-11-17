
from typing import TypedDict, Optional, Annotated
import operator
import uuid

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

from app.agent_loop import parse_agent_decision
from app.rag import generate_rag_answer
from app.tools import course_plan_checker


# Keep providers outside checkpointed graph state.
PROVIDERS = {}


class AgentState(TypedDict):
    question: str
    tool: Optional[str]
    course_ids: list[str]
    available_hours_per_week: Optional[float]
    answer: Optional[str]
    sources: list[dict]
    data: Optional[dict]
    conversation_history: Annotated[list[str], operator.add]


def get_provider(config):
    thread_id = config["configurable"]["thread_id"]
    provider = PROVIDERS.get(thread_id)

    if provider is None:
        raise ValueError("Provider not found for this conversation.")

    return provider


def agent_node(state: AgentState, config):
    question = state["question"]
    provider = get_provider(config)

    history = "\n".join(state["conversation_history"])

    prompt = f"""
You are the tool-selection agent for NPTELPicker.

Choose exactly one tool.

AVAILABLE TOOLS:

1. rag
Use for course information, recommendations,
comparisons and general NPTEL questions.

2. course_plan
Use for checking selected courses,
calculating credits and estimating workload.

Extract:
- course_ids: list of course IDs
- available_hours_per_week: number or null

Return ONLY valid JSON.

Example:
{{
    "tool": "course_plan",
    "course_ids": ["noc26_cs169"],
    "available_hours_per_week": 8
}}

CONVERSATION HISTORY:
{history}

CURRENT QUESTION:
{question}
"""

    response = provider.generate_response(prompt)
    decision = parse_agent_decision(response)

    return {
        "tool": decision["tool"],
        "course_ids": decision.get("course_ids") or [],
        "available_hours_per_week":
            decision.get("available_hours_per_week")
    }


def rag_node(state: AgentState, config):
    provider = get_provider(config)

    result = generate_rag_answer(
        question=state["question"],
        provider=provider,
        top_k=5
    )

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "data": None
    }


def course_plan_node(state: AgentState):
    course_ids = state.get("course_ids") or []
    available_hours = state.get("available_hours_per_week")

    if not course_ids:
        return {
            "answer": "Please provide the NPTEL course IDs you want to include in your plan.",
            "data": None,
            "sources": []
        }

    if available_hours is None:
        return {
            "answer": "How many study hours can you spend per week?",
            "data": None,
            "sources": []
        }

    approval = interrupt({
        "message": "Approval required before checking the course plan.",
        "course_ids": course_ids,
        "available_hours_per_week": available_hours
    })

    if not isinstance(approval, dict) or approval.get("approved") is not True:
        return {
            "answer": "Course plan execution was not approved.",
            "data": None,
            "sources": []
        }

    result = course_plan_checker(
        course_ids=course_ids,
        available_hours_per_week=available_hours
    )

    return {
        "answer": "Your course plan has been checked successfully.",
        "data": result,
        "sources": []
    }


def route_tool(state: AgentState):
    if state["tool"] == "rag":
        return "rag"

    return "course_plan"


def build_agent_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent_node)
    workflow.add_node("rag", rag_node)
    workflow.add_node("course_plan", course_plan_node)

    workflow.add_edge(START, "agent")

    workflow.add_conditional_edges(
        "agent",
        route_tool,
        {
            "rag": "rag",
            "course_plan": "course_plan"
        }
    )

    workflow.add_edge("rag", END)
    workflow.add_edge("course_plan", END)

    memory = InMemorySaver()

    return workflow.compile(checkpointer=memory)


AGENT_GRAPH = build_agent_graph()


def run_graph(question: str, provider, thread_id: Optional[str] = None):
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if thread_id is None:
        thread_id = str(uuid.uuid4())

    PROVIDERS[thread_id] = provider

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "question": question,
        "tool": None,
        "course_ids": [],
        "available_hours_per_week": None,
        "answer": None,
        "sources": [],
        "data": None,
        "conversation_history": [question]
    }

    return AGENT_GRAPH.invoke(initial_state, config=config)


def resume_graph(thread_id: str, approved: bool):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    return AGENT_GRAPH.invoke(
        Command(resume={"approved": approved}),
        config=config
    )
