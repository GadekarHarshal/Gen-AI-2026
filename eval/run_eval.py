
import json
import re
import sys
import time
import uuid
from pathlib import Path

import chromadb
from google.genai import errors

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.chunking import chunk_documents
from app.embed import generate_embeddings, generate_embedding
from app.llm_provider import GeminiProvider


EVAL_FILE = PROJECT_ROOT / "eval" / "eval_set.json"
RESULT_FILE = PROJECT_ROOT / "eval" / "eval_results.json"
TEMP_DB_PATH = PROJECT_ROOT / "data" / "eval_chroma_db"


CONFIGURATIONS = {
    "Config A": {
        "chunk_size": 250,
        "overlap": 25,
        "top_k": 3
    },
    "Config B": {
        "chunk_size": 500,
        "overlap": 50,
        "top_k": 5
    }
}


UNKNOWN_PHRASES = [
    "i don't know",
    "does not contain the answer",
    "not available",
    "not provided",
    "insufficient information",
    "cannot determine from the available information"
]


def load_questions():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_context(question, collection, top_k):

    if collection.count() == 0:
        return "", []

    query_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count())
    )

    context_parts = []
    sources = []

    if results["ids"] and results["ids"][0]:

        for index, document in enumerate(results["documents"][0]):

            metadata = results["metadatas"][0][index]
            title = metadata.get("title", "Unknown Course")

            context_parts.append(
                f"[{index + 1}]\n"
                f"Course: {title}\n"
                f"Information:\n{document}"
            )

            sources.append(title)

    return "\n\n".join(context_parts), sources


def generate_answer(question, context, provider):

    prompt = f"""
You are NPTELPicker, an NPTEL course assistant.

Answer the student's question using ONLY the retrieved context.

STRICT RULES:

1. Never use outside knowledge.
2. Never invent course information.
3. If the requested information is missing,
   respond with exactly:

   I don't know. The available course information does not contain the answer.

4. Do not invent examination dates or examination centres.
5. Do not invent credit information or credit-transfer policies.
6. Do not assume that a course is suitable for a particular
   academic year unless the context supports it.
7. Cite supporting information using [1], [2], etc.
8. Keep the answer simple and clear.

RETRIEVED CONTEXT:

{context}

STUDENT QUESTION:

{question}

Return only the answer.
"""

    # Respect the Gemini Free Tier request rate.
    time.sleep(5)

    # Retry temporary rate-limit errors.
    for attempt in range(3):
        try:
            return provider.generate_response(prompt)

        except errors.APIError as error:
            if error.code == 429 and attempt < 2:
                wait_time = 15 * (attempt + 1)

                print(
                    f"Rate limit reached. "
                    f"Waiting {wait_time} seconds..."
                )

                time.sleep(wait_time)
            else:
                raise

    raise RuntimeError("Gemini answer generation failed.")


def check_expected_behavior(answer, expected_behavior):

    answer_lower = answer.lower()

    says_unknown = any(
        phrase in answer_lower
        for phrase in UNKNOWN_PHRASES
    )

    has_citation = bool(
        re.search(r"\[\d+\]", answer)
    )

    if expected_behavior == "say_unknown":

        return {
            "passed": says_unknown,
            "reason": (
                "Correctly identified missing information."
                if says_unknown
                else "Expected an unknown response."
            )
        }

    if expected_behavior == "answer_from_context":

        passed = has_citation and not says_unknown

        return {
            "passed": passed,
            "reason": (
                "Answer contains citations."
                if passed
                else "Answer is missing citations or says unknown."
            )
        }

    return {
        "passed": False,
        "reason": "Unknown evaluation category."
    }


def create_collection(config_name, chunks):

    client = chromadb.PersistentClient(
        path=str(TEMP_DB_PATH)
    )

    collection_name = (
        f"eval_{config_name.lower().replace(' ', '_')}_"
        f"{uuid.uuid4().hex[:8]}"
    )

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    if chunks:

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            chunk["metadata"]
            for chunk in chunks
        ]

        ids = [
            f"chunk_{i}"
            for i in range(len(chunks))
        ]

        embeddings = generate_embeddings(documents)

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings
        )

    return client, collection


def evaluate_configuration(
    name,
    settings,
    questions,
    provider
):

    print(f"\nStarting {name}...")

    chunks = chunk_documents(
        chunk_size=settings["chunk_size"],
        overlap=settings["overlap"]
    )

    print("Total chunks:", len(chunks))

    client, collection = create_collection(
        name,
        chunks
    )

    results = []
    passed = 0

    try:

        for item in questions:

            question = item["question"]

            context, sources = retrieve_context(
                question,
                collection,
                settings["top_k"]
            )

            answer = generate_answer(
                question,
                context,
                provider
            )

            evaluation = check_expected_behavior(
                answer,
                item["expected_behavior"]
            )

            if evaluation["passed"]:
                passed += 1

            results.append({
                "id": item["id"],
                "question": question,
                "expected_behavior": item["expected_behavior"],
                "answer": answer,
                "sources": sources,
                "passed": evaluation["passed"],
                "evaluation_reason": evaluation["reason"]
            })

            status = (
                "PASS"
                if evaluation["passed"]
                else "REVIEW"
            )

            print(
                f"Question {item['id']}: {status}"
            )

    finally:
        client.delete_collection(collection.name)

    total = len(questions)

    accuracy = (
        (passed / total) * 100
        if total > 0
        else 0
    )

    summary = {
        "configuration": name,
        "settings": settings,
        "total_questions": total,
        "passed": passed,
        "failed_or_review": total - passed,
        "accuracy_percentage": round(accuracy, 2),
        "results": results
    }

    print(
        f"\n{name} accuracy: {accuracy:.2f}%"
    )

    return summary


def main():

    questions = load_questions()

    if not questions:
        print("No evaluation questions found.")
        return

    provider = GeminiProvider()

    all_results = []

    for name, settings in CONFIGURATIONS.items():

        result = evaluate_configuration(
            name,
            settings,
            questions,
            provider
        )

        all_results.append(result)

    with open(
        RESULT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_results,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nEvaluation completed.")

    print(
        f"Results saved to: {RESULT_FILE}"
    )

    print("\nCONFIGURATION COMPARISON")

    for result in all_results:

        print(
            result["configuration"],
            "| Chunk size:",
            result["settings"]["chunk_size"],
            "| Overlap:",
            result["settings"]["overlap"],
            "| Top-K:",
            result["settings"]["top_k"],
            "| Accuracy:",
            f"{result['accuracy_percentage']}%"
        )


if __name__ == "__main__":
    main()
