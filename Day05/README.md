# Day 05 – LLM Fundamentals and Preparation

## Objective

Understand the fundamentals of Large Language Models (LLMs) and prepare NPTELPicker for future AI integration.

## Tasks Completed

1. Studied how Large Language Models work.
2. Learned about tokens and Transformers.
3. Understood prompt engineering.
4. Learned about APIs and RAG.
5. Understood AI hallucinations.
6. Prepared 10 sample user questions for NPTELPicker.

## Project Structure

```text
Day05/
│
├── docs/
│   └── how_llms_work.md
│
├── questions.md
└── README.md
```

## Files Description

- `docs/how_llms_work.md` – Explains LLM fundamentals, Transformers, tokens, APIs, RAG and hallucinations.
- `questions.md` – Contains 10 sample questions to evaluate NPTELPicker.
- `README.md` – Day 5 project documentation.

## Next Steps

- Test the existing FastAPI application.
- Understand API endpoints and their working.
- Prepare for LLM integration in Day 6.

## Status

Day 5 documentation and sample question preparation completed.


## API Testing Results

The existing FastAPI application was tested using Swagger UI.

| Endpoint | Method | Result |
|---|---|---|
| `/health` | GET | 200 OK |
| `/records` | GET | 200 OK |
| `/records/{course_id}` | GET | 200 OK |
| `/search` | GET | 200 OK |
| `/questions` | POST | 200 OK |

### Testing Observations

- Health check successfully returned the healthy status.
- Records endpoint returned course information.
- Course ID endpoint successfully retrieved individual course details.
- Smart search returned relevant course results.
- Questions endpoint successfully received and acknowledged student questions.

### Important Note

The current questions endpoint only acknowledges received questions. LLM integration and AI-generated answers are planned for Day 6.

### Day 5 Final Status

- [x] LLM fundamentals documentation
- [x] Prepared 10 sample questions
- [x] Created Day 5 README
- [x] Started FastAPI application
- [x] Tested all five API endpoints
- [x] Verified successful API responses

## Auditor Feedback Corrections

The following improvements were made based on the Day 5 evaluation:

1. Added an LLM workflow diagram showing Prompt → Tokens → Model → Answer.
2. Added an unanswerable evaluation question (Q6).
3. Explained why the current course dataset cannot answer Q6.
4. Added the LLM documentation at the repository root under `docs/how_llms_work.md`.

## Unanswerable Question Evaluation

Q6 asks for the exact examination date and examination centre of a course.

The current dataset does not contain these details. Therefore, NPTELPicker should respond that the information is unavailable rather than generating an unsupported answer.

## Checkpoint

Checkpoint 1 represents the completion of LLM fundamentals, sample question preparation, and API testing.

The `checkpoint-1` Git tag will identify this stage of the project.