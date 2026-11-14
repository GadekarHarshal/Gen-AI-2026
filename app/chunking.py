
import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"


def load_documents():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    documents = []

    for record in records:
        text = (
            f"Course Name: {record.get('course_name', '')}\n"
            f"Course ID: {record.get('course_id', '')}\n"
            f"Discipline: {record.get('discipline', '')}\n"
            f"Institution: {record.get('institute', '')}\n"
            f"Duration: {record.get('duration_weeks', '')} weeks\n"
            f"Level: {record.get('level', '')}\n"
            f"Course URL: {record.get('course_url', '')}"
        )

        documents.append({
            "text": text,
            "metadata": {
                "source": "data/records.json",
                "page": "not_applicable",
                "title": record.get("course_name", "Untitled Course")
            }
        })

    return documents


def split_text(text, chunk_size=500, overlap=50):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def chunk_documents(chunk_size=500, overlap=50):
    documents = load_documents()
    chunks = []

    for document in documents:
        text_chunks = split_text(document["text"], chunk_size, overlap)

        for chunk in text_chunks:
            chunks.append({
                "text": chunk,
                "metadata": document["metadata"].copy()
            })

    return chunks
