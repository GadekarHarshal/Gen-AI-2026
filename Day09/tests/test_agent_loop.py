
import pytest

from app.agent_loop import parse_agent_decision, run_agent


class FakeProvider:
    """Simulates Gemini responses without making API calls."""

    def __init__(self, response):
        self.response = response

    def generate_response(self, prompt):
        return self.response


def test_parse_rag_decision():
    response = '{"tool": "rag"}'

    result = parse_agent_decision(response)

    assert result["tool"] == "rag"


def test_parse_course_plan_decision():
    response = """
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"],
        "available_hours_per_week": 8
    }
    """

    result = parse_agent_decision(response)

    assert result["tool"] == "course_plan"
    assert result["course_ids"] == ["noc26_cs169"]
    assert result["available_hours_per_week"] == 8


def test_invalid_tool_decision():
    response = '{"tool": "invalid"}'

    with pytest.raises(ValueError):
        parse_agent_decision(response)


def test_course_plan_agent():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"],
        "available_hours_per_week": 8
    }
    """)

    result = run_agent(
        "Check my course plan",
        provider
    )

    assert result["tool_used"] == "course_plan"
    assert result["data"]["total_courses"] == 1
    assert result["data"]["total_credits"] == 3


def test_agent_asks_for_missing_course_ids():
    provider = FakeProvider('{"tool": "course_plan"}')

    result = run_agent(
        "Check my course plan",
        provider
    )

    assert result["data"] is None
    assert "course IDs" in result["answer"]


def test_agent_asks_for_missing_hours():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"]
    }
    """)

    result = run_agent(
        "Check my course plan",
        provider
    )

    assert result["data"] is None
    assert "study hours" in result["answer"]


def test_rag_agent(monkeypatch):
    import app.agent_loop as agent_module

    def fake_rag(question, provider, top_k=5):
        return {
            "answer": "Artificial Intelligence: Foundations and Algorithms [1]",
            "sources": [
                {
                    "citation": "[1]",
                    "title": "Artificial Intelligence: Foundations and Algorithms",
                    "source": "data/records.json"
                }
            ]
        }

    monkeypatch.setattr(
        agent_module,
        "generate_rag_answer",
        fake_rag
    )

    provider = FakeProvider('{"tool": "rag"}')

    result = agent_module.run_agent(
        "Which courses cover artificial intelligence?",
        provider
    )

    assert result["tool_used"] == "rag"
    assert "[1]" in result["answer"]
    assert len(result["sources"]) == 1