
import json

from fastapi.testclient import TestClient

from Day06.app import main


client = TestClient(main.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_chat_success(monkeypatch):
    class FakeGemini:
        def generate_response(self, prompt):
            return json.dumps({
                "answer": "AI for Earth Observation is an available course.",
                "confidence": 0.95,
                "follow_up": "Would you like more AI courses?"
            })

    monkeypatch.setattr(main, "gemini", FakeGemini())

    response = client.post(
        "/chat",
        json={
            "question": "Suggest an AI course"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "confidence" in data
    assert "follow_up" in data


def test_short_question():
    response = client.post(
        "/chat",
        json={
            "question": "AI"
        }
    )

    assert response.status_code == 422


def test_empty_question():
    response = client.post(
        "/chat",
        json={
            "question": " "
        }
    )

    assert response.status_code == 422
