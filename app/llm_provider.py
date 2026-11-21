
import logging
import os
import time
from collections import OrderedDict
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / "Day06" / ".env"

load_dotenv(ENV_FILE)

logger = logging.getLogger(__name__)

CACHE_MAX_SIZE = 100


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

        self.response_cache = OrderedDict()

    def generate_response(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        cache_key = prompt.strip()

        # Check response cache
        if cache_key in self.response_cache:
            self.response_cache.move_to_end(cache_key)

            logger.info(
                "Cache HIT | model=%s",
                self.model
            )

            return self.response_cache[cache_key]

        logger.info(
            "Cache MISS | model=%s",
            self.model
        )

        start_time = time.perf_counter()

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                latency_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                usage = response.usage_metadata

                input_tokens = (
                    usage.prompt_token_count if usage else None
                )

                output_tokens = (
                    usage.candidates_token_count if usage else None
                )

                total_tokens = (
                    usage.total_token_count if usage else None
                )

                if not response.text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                result = response.text.strip()

                logger.info(
                    "Gemini request completed | "
                    "model=%s | latency_ms=%.2f | "
                    "input_tokens=%s | output_tokens=%s | "
                    "total_tokens=%s",
                    self.model,
                    latency_ms,
                    input_tokens,
                    output_tokens,
                    total_tokens
                )

                # Store response in cache
                self.response_cache[cache_key] = result

                # Remove oldest entry if cache is full
                if len(self.response_cache) > CACHE_MAX_SIZE:
                    self.response_cache.popitem(last=False)

                return result

            except errors.APIError as error:
                if error.code not in (429, 500, 503):
                    raise

                if attempt == 2:
                    raise

                time.sleep(2 ** attempt)

        raise RuntimeError("Gemini request failed.")
