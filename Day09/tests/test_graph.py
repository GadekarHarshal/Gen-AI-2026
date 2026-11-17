
import pytest

import app.graph as graph_module
from app.graph import run_graph, resume_graph


class FakeProvider:
    def __init__(self, response):
        self.response = response

    def generate_response(self, prompt):
        return self.response


def test_graph_course_plan_requires_approval():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"],
        "available_hours_per_week": 8
    }
    """)

    result = run_graph(
        "Check my course plan",
        provider,
        thread_id="course-plan-test"
    )

    assert result["__interrupt__"]
    approval_data = result["__interrupt__"][0].value
    assert approval_data["course_ids"] == ["noc26_cs169"]


def test_graph_course_plan_approved():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"],
        "available_hours_per_week": 8
    }
    """)

    run_graph(
        "Check my course plan",
        provider,
        thread_id="approved-plan-test"
    )

    result = resume_graph(
        "approved-plan-test",
        approved=True
    )

    assert result["data"]["total_courses"] == 1
    assert result["data"]["total_credits"] == 3
    assert "successfully" in result["answer"]


def test_graph_course_plan_rejected():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"],
        "available_hours_per_week": 8
    }
    """)

    run_graph(
        "Check my course plan",
        provider,
        thread_id="rejected-plan-test"
    )

    result = resume_graph(
        "rejected-plan-test",
        approved=False
    )

    assert result["data"] is None
    assert "not approved" in result["answer"]


def test_graph_rag(monkeypatch):
    def fake_rag(question, provider, top_k=5):
        return {
            "answer": "Artificial Intelligence course [1]",
            "sources": [
                {"citation": "[1]", "title": "AI Course"}
            ]
        }

    monkeypatch.setattr(
        graph_module,
        "generate_rag_answer",
        fake_rag
    )

    provider = FakeProvider('{"tool": "rag"}')

    result = run_graph(
        "Which courses cover artificial intelligence?",
        provider,
        thread_id="rag-test"
    )

    assert result["tool"] == "rag"
    assert "[1]" in result["answer"]
    assert len(result["sources"]) == 1


def test_graph_missing_course_ids():
    provider = FakeProvider('{"tool": "course_plan"}')

    result = run_graph(
        "Check my course plan",
        provider,
        thread_id="missing-ids-test"
    )

    assert result["data"] is None
    assert "course IDs" in result["answer"]


def test_graph_missing_study_hours():
    provider = FakeProvider("""
    {
        "tool": "course_plan",
        "course_ids": ["noc26_cs169"]
    }
    """)

    result = run_graph(
        "Check my course plan",
        provider,
        thread_id="missing-hours-test"
    )

    assert result["data"] is None
    assert "study hours" in result["answer"]


def test_graph_empty_question():
    provider = FakeProvider('{"tool": "rag"}')

    with pytest.raises(ValueError, match="Question cannot be empty"):
        run_graph("", provider)
