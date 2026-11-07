import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path("data/records.json")


def smart_search(query):
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = json.load(file)

    courses = []

    for record in records:
        text = (
            record["course_name"] + " " +
            record["discipline"] + " " +
            record["institute"]
        )
        courses.append(text)

    vectorizer = TfidfVectorizer()
    course_vectors = vectorizer.fit_transform(courses)

    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, course_vectors)[0]

    results = []

    for i in scores.argsort()[::-1]:
        if scores[i] > 0:
            results.append({
                "course": records[i],
                "similarity": round(float(scores[i]), 3)
            })

    return results