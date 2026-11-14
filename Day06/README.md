
# Day 06 - Gemini AI Integration

## Project Overview

NPTELPicker is an AI-powered NPTEL course recommendation assistant.

Day 06 integrates Google Gemini with FastAPI to answer student questions using the available NPTEL course dataset.

## Objectives

- Integrate Google Gemini using the official Python SDK.
- Securely manage API keys using environment variables.
- Create a Gemini provider wrapper.
- Build a FastAPI chat endpoint.
- Generate structured JSON responses.
- Validate requests and responses using Pydantic.
- Test API functionality using pytest.

## Project Structure

```text
Day06/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- llm_provider.py
|   |-- schemas.py
|
|-- prompts/
|   |-- system_prompt.txt
|
|-- tests/
|   |-- test_chat.py
|
|-- .env
|-- .env.example
|-- README.md
|-- requirements.txt
```

## Technologies Used

- Python
- FastAPI
- Google Gemini API
- Google GenAI SDK
- Pydantic
- Python Dotenv
- Pytest
- HTTPX

## Environment Setup

1. Activate the project's virtual environment.

2. Install dependencies:

```bash
pip install -r Day06/requirements.txt
```

3. Create a `.env` file inside Day06.

4. Add the following configuration:

```env
GEMINI_API_KEY=your_actual_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

5. Never upload the actual `.env` file to GitHub.

## Run the Application

From the project root, execute:

```bash
uvicorn Day06.app.main:app --reload --port 8001
```

Open Swagger UI:

http://127.0.0.1:8001/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Welcome message |
| GET | /health | Health check |
| POST | /chat | Ask an NPTEL question |

## Chat Request Example

```json
{
    "question": "Suggest an NPTEL course for AI students."
}
```

## Chat Response Example

```json
{
    "answer": "Here are some relevant NPTEL courses...",
    "confidence": 0.95,
    "follow_up": "Would you like to compare these courses?"
}
```

## AI Assistant Features

- Uses Google Gemini for response generation.
- Supplies available NPTEL course records as context.
- Provides course recommendations and comparisons.
- Returns structured JSON responses.
- Identifies information missing from the dataset.
- Uses Pydantic for input and output validation.
- Includes retry handling for temporary Gemini API errors.

## Testing

Run automated tests:

```bash
python -m pytest Day06/tests/test_chat.py -v
```

### Verified Test Results

- Home endpoint test: Passed
- Health endpoint test: Passed
- Chat response test: Passed
- Short question validation: Passed
- Empty question validation: Passed

Total: 5 tests passed.

Real Gemini API responses were also tested separately using Swagger UI.

## Security

- API key stored in `.env`.
- `.env` excluded using `.gitignore`.
- `.env.example` provided as a safe configuration template.
- API credentials are not included in source code.

## Day 06 Status

Gemini integration, FastAPI chat endpoint, structured responses, input validation, and automated tests implemented and tested.

## Next Steps

- Improve retrieval and grounding using embeddings.
- Introduce vector search.
- Build the RAG pipeline.
- Improve answer accuracy with source-based retrieval.



## Prompt Engineering and Evaluation

The prompt files are maintained in the repository-level `prompts/` directory.

### Prompt Files

- `prompts/system_prompt.txt` – Main NPTELPicker instructions.
- `prompts/course_recommendation.txt` – Task-specific course recommendation instructions.
- `prompts/course_comparison.txt` – Task-specific course comparison instructions.

### Prompt Comparison

The prompt comparison is documented in:

`eval/prompt_compare.md`

It compares two prompt versions using 10 predefined NPTELPicker questions from `Day05/questions.md`.

### Application Structure

The FastAPI application is maintained in the repository-level `app/` directory.

Run the application from the repository root:

```bash
uvicorn app.main:app --reload --port 8001
```

Open Swagger UI:

`http://127.0.0.1:8001/docs`

### Automated Tests

Run:

```bash
python -m pytest Day06/tests/test_chat.py -v
```
