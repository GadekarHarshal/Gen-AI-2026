
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors


DAY06_FOLDER = Path(__file__).resolve().parents[1]
ENV_FILE = DAY06_FOLDER / ".env"

load_dotenv(ENV_FILE)


class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        )

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Check Day06/.env."
            )

        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return response.text.strip()

            except errors.APIError as error:
                if error.code not in (429, 500, 503):
                    raise

                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        raise RuntimeError("Gemini request failed.")
