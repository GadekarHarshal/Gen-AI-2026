
import pytest
from fastapi.testclient import TestClient

import app.main as main_module
import app.rag as rag_module
import app.vectorstore as vectorstore_module
from app.main import app
from app.records import (
    count_by,
    get_by_id,
    load_records,
    search,
)
from app.tools import course_plan_checker

client = TestClient(app)


# ==========================================
# FAKE LLM PROVIDER
# ==========================================

class FakeLLM:

    def generate_response(self, prompt):

        assert "STUDENT QUESTION:" in prompt

        return (
            "Advanced Distributed Systems is a "
            "12-week course [1]."
        )


# ==========================================
# COURSE RECORD TESTS
# ==========================================

def test_load_records():

    records = load_records()

    assert isinstance(records, list)
    assert len(records) > 0


def test_search_existing_course():

    results = search("Advanced Distributed Systems")

    assert len(results) >= 1

    assert (
        results[0]["course_name"]
        == "Advanced Distributed Systems"
    )


def test_search_non_existing_course():

    results = search("Non Existing Course XYZ")

    assert results == []


def test_get_existing_course():

    course = get_by_id("noc26_cs169")

    assert course is not None

    assert (
        course["course_name"]
        == "Advanced Distributed Systems"
    )


def test_get_non_existing_course():

    course = get_by_id("invalid_course_id")

    assert course is None


def test_count_by_discipline():

    counts = count_by("discipline")

    assert isinstance(counts, dict)
    assert len(counts) > 0


# ==========================================
# FASTAPI HEALTH TEST
# ==========================================

def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "healthy"


# ==========================================
# RAG /ASK TEST WITH FAKE LLM
# ==========================================

def test_ask_endpoint_with_fake_llm(monkeypatch):

    fake_results = [
        {
            "text": (
                "Advanced Distributed Systems "
                "has a duration of 12 weeks."
            ),
            "metadata": {
                "title": "Advanced Distributed Systems",
                "source": "data/records.json",
            },
        }
    ]

    monkeypatch.setattr(
        main_module,
        "gemini",
        FakeLLM()
    )

    monkeypatch.setattr(
        vectorstore_module,
        "get_collection_count",
        lambda: 1
    )

    monkeypatch.setattr(
        rag_module,
        "semantic_search",
        lambda question, top_k=5: fake_results
    )

    response = client.post(
        "/ask",
        json={
            "question": (
                "What is the duration of "
                "Advanced Distributed Systems?"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    answer = data["answer"].lower()

    assert (
        "12 weeks" in answer
        or "12-week" in answer
    )

    assert len(data["sources"]) == 1

    assert (
        data["sources"][0]["title"]
        == "Advanced Distributed Systems"
    )


def test_ask_endpoint_when_database_is_empty(monkeypatch):

    monkeypatch.setattr(
        main_module,
        "gemini",
        FakeLLM()
    )

    monkeypatch.setattr(
        vectorstore_module,
        "get_collection_count",
        lambda: 0
    )

    response = client.post(
        "/ask",
        json={
            "question": "Tell me about NPTEL courses."
        }
    )

    assert response.status_code == 503


# ==========================================
# AGENT TOOL TESTS
# ==========================================

def test_course_plan_checker():

    result = course_plan_checker(
        course_ids=["noc26_cs169"],
        available_hours_per_week=10
    )

    assert result["total_courses"] == 1
    assert result["total_credits"] == 3
    assert result["estimated_hours_per_week"] == 3

    assert (
        result["workload_status"]
        == "Sufficient study hours"
    )


def test_course_plan_checker_invalid_course():

    with pytest.raises(ValueError):

        course_plan_checker(
            course_ids=["invalid_course_id"],
            available_hours_per_week=10
        )


def test_course_plan_checker_without_courses():

    with pytest.raises(ValueError):

        course_plan_checker(
            course_ids=[],
            available_hours_per_week=10
        )
