
import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEEDBACK_FILE = PROJECT_ROOT / "data" / "feedback.json"


def save_feedback(question, answer, feedback_type):
    """
    Save user feedback permanently in data/feedback.json.
    """

    if feedback_type not in ["positive", "negative"]:
        raise ValueError("Invalid feedback type.")

    FEEDBACK_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    feedback_record = {
        "question": question,
        "answer": answer,
        "feedback": feedback_type,
        "timestamp": datetime.now().astimezone().isoformat()
    }

    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                records = []

        except (json.JSONDecodeError, OSError):
            records = []
    else:
        records = []

    records.append(feedback_record)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    return feedback_record
