from fastapi import FastAPI, HTTPException
from app.records import load_records, search, get_by_id
from Day04.app.smart_search import smart_search

app = FastAPI(title="NPTELPicker API")


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/records")
def get_records(limit: int = 20):
    records = load_records()
    return records[:limit]


@app.get("/records/{course_id}")
def get_record(course_id: str):
    record = get_by_id(course_id)

    if record is None:
        raise HTTPException(status_code=404, detail="Course not found")

    return record


@app.get("/search")
def search_records(q: str):
    return smart_search(q)


@app.post("/questions")
def ask_question(question: str):
    return {
        "question": question,
        "message": "Question received successfully"
    }