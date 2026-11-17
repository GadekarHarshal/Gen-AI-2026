
import json
import re

from app.rag import generate_rag_answer
from app.tools import course_plan_checker


def parse_agent_decision(response):
    """Convert Gemini's JSON response into a Python dictionary."""

    response = response.strip()

    if response.startswith("```"):
        response = re.sub(r"^```(?:json)?\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

    try:
        decision = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError("Agent returned invalid JSON.") from error

    if decision.get("tool") not in ["rag", "course_plan"]:
        raise ValueError("Agent selected an unsupported tool.")

    return decision


def run_agent(question, provider):
    """Select and execute the appropriate NPTELPicker tool."""

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    decision_prompt = f"""
You are the tool-selection agent for NPTELPicker.

Choose exactly one tool based on the student's question.

AVAILABLE TOOLS:

1. rag
Use for:
- NPTEL course information
- Course recommendations
- Course comparisons
- Course-related questions

2. course_plan
Use for:
- Checking a student's selected courses
- Calculating credits
- Estimating study workload
- Checking available study hours

Extract the following information when available:
- course_ids: list of course IDs
- available_hours_per_week: number of study hours

If the student asks for course planning but information
is missing, still select course_plan and return the
information you can identify.

Return ONLY valid JSON in this format:

{{
    "tool": "rag",
    "course_ids": [],
    "available_hours_per_week": null
}}

OR

{{
    "tool": "course_plan",
    "course_ids": ["noc26_cs169"],
    "available_hours_per_week": 8
}}

STUDENT QUESTION:
{question}
"""

    decision_response = provider.generate_response(decision_prompt)
    decision = parse_agent_decision(decision_response)

    if decision["tool"] == "rag":

        result = generate_rag_answer(
            question=question,
            provider=provider,
            top_k=5
        )

        return {
            "tool_used": "rag",
            "answer": result["answer"],
            "sources": result["sources"]
        }

    if decision["tool"] == "course_plan":

        course_ids = decision.get("course_ids") or []
        available_hours = decision.get(
            "available_hours_per_week"
        )

        if not course_ids:
            return {
                "tool_used": "course_plan",
                "answer": "Please provide the NPTEL course IDs you want to include in your plan.",
                "data": None
            }

        if available_hours is None:
            return {
                "tool_used": "course_plan",
                "answer": "How many study hours can you spend per week?",
                "data": None
            }

        result = course_plan_checker(
            course_ids=course_ids,
            available_hours_per_week=available_hours
        )

        return {
            "tool_used": "course_plan",
            "answer": "Your course plan has been checked successfully.",
            "data": result
        }
