
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


ENV_FILE = Path(__file__).resolve().parent.parent / "Day06" / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in Day06/.env")

client = genai.Client(api_key=api_key)

EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embedding(text):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return result.embeddings[0].values


def generate_embeddings(texts):
    embeddings = []

    for text in texts:
        embeddings.append(generate_embedding(text))

    return embeddings
