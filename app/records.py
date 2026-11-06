import json
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent / "data" / "records.json"


def load_records():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def search(keyword):
    records = load_records()
    results = []

    for course in records:
        if keyword.lower() in course["course_name"].lower():
            results.append(course)

    return results


def count_by(category):
    records = load_records()
    counts = {}

    for course in records:
        value = course.get(category)

        if value:
            counts[value] = counts.get(value, 0) + 1

    return counts


def get_by_id(course_id):
    records = load_records()

    for course in records:
        if course["course_id"] == course_id:
            return course

    return None