
import json
import pytest

from ui import feedback


def test_save_positive_feedback(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback.json"
    monkeypatch.setattr(feedback, "FEEDBACK_FILE", feedback_file)

    feedback.save_feedback(
        "What is the course duration?",
        "12 weeks",
        "positive"
    )

    with open(feedback_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    assert len(records) == 1
    assert records[0]["feedback"] == "positive"


def test_save_negative_feedback(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback.json"
    monkeypatch.setattr(feedback, "FEEDBACK_FILE", feedback_file)

    feedback.save_feedback(
        "Which institute offers this course?",
        "IIT Delhi",
        "negative"
    )

    with open(feedback_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    assert records[0]["feedback"] == "negative"


def test_append_multiple_feedback_records(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback.json"
    monkeypatch.setattr(feedback, "FEEDBACK_FILE", feedback_file)

    feedback.save_feedback("Question 1", "Answer 1", "positive")
    feedback.save_feedback("Question 2", "Answer 2", "negative")

    with open(feedback_file, "r", encoding="utf-8") as file:
        records = json.load(file)

    assert len(records) == 2


def test_invalid_feedback_type(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback.json"
    monkeypatch.setattr(feedback, "FEEDBACK_FILE", feedback_file)

    with pytest.raises(ValueError):
        feedback.save_feedback(
            "Question",
            "Answer",
            "neutral"
        )
