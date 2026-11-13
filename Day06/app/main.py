
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from google.genai import errors

from Day06.app.llm_provider import GeminiProvider
from Day06.app.schemas import ChatRequest, ChatResponse


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = PROJECT_ROOT / "data" / "records.json"
PROMPT_FILE = PROJECT_ROOT / "Day06" / "prompts" / "system_prompt.txt"


# Create FastAPI application
app = FastAPI(
    title="NPTELPicker Day 6",
    description="AI-powered NPTEL course assistant using Google Gemini",
    version="1.0.0"
)


# Load course records
def load_courses():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Unable to load course records: {error}"
        )


# Load system prompt
def load_system_prompt():
    try:
        return PROMPT_FILE.read_text(encoding="utf-8")

    except OSError as error:
        raise RuntimeError(
            f"Unable to load system prompt: {error}"
        )


# Initialize Gemini provider
try:
    gemini = GeminiProvider()
except ValueError as error:
    gemini = None
    print(f"Gemini configuration error: {error}")


@app.get("/")
def home():
    return {
        "message": "Welcome to NPTELPicker AI Assistant",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "provider": "Google Gemini"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    if gemini is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini API is not configured."
        )

    try:
        courses = load_courses()
        system_prompt = load_system_prompt()

        course_context = json.dumps(
            courses,
            ensure_ascii=False,
            indent=2
        )

        full_prompt = f"""
{system_prompt}

AVAILABLE NPTEL COURSE DATA:
{course_context}

STUDENT QUESTION:
{request.question}

Return only the required JSON response.
"""

        result = gemini.generate_response(full_prompt)

        # Parse Gemini JSON response
        try:
            result = result.strip()

            if result.startswith("```"):
                result = result.replace("```json", "")
                result = result.replace("```", "")
                result = result.strip()

            response_data = json.loads(result)

            return ChatResponse(**response_data)

        except (json.JSONDecodeError, ValueError) as error:
            raise HTTPException(
                status_code=502,
                detail=f"Gemini returned an invalid response: {error}"
            )

    except HTTPException:
        raise

    except errors.APIError as error:
        raise HTTPException(
            status_code=503,
            detail=f"Gemini API unavailable: {error}"
        )

    except (RuntimeError, OSError) as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
