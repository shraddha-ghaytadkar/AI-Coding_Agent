"""
Unified Groq / xAI Grok LLM Provider implementation.
Seamlessly supports both Groq Cloud (gsk_...) and xAI Grok (xai-...) keys with automatic endpoint routing,
automatic retry mechanism, and zero hardcoded replies.
Follows Open/Closed Principle (OCP) and Liskov Substitution Principle (LSP).
"""
import time
import logging
import requests
from typing import Optional
from core.exceptions import LLMProviderError
from services.llm.base import BaseLLMProvider

logger = logging.getLogger("GrokLLMProvider")


class GrokLLMProvider(BaseLLMProvider):
    """
    Concrete LLM provider auto-routing between:
    - Groq Cloud (keys starting with 'gsk_') -> https://api.groq.com/openai/v1
    - xAI Grok (keys starting with 'xai-')   -> https://api.x.ai/v1
    """

    GROQ_CLOUD_URL = "https://api.groq.com/openai/v1/chat/completions"
    XAI_GROK_URL = "https://api.x.ai/v1/chat/completions"

    def __init__(self, api_key: str, model_name: Optional[str] = None, max_retries: int = 3):
        super().__init__(provider_name="Groq/Grok AI")
        self.api_key = api_key.strip() if api_key else ""
        self.max_retries = max_retries

        # Auto-detect endpoint and model based on key prefix
        if self.api_key.startswith("gsk_"):
            self.base_url = self.GROQ_CLOUD_URL
            self.model_name = model_name if (model_name and "grok" not in model_name.lower()) else "openai/gpt-oss-120b"
            self.provider_label = "Groq Cloud"
        else:
            self.base_url = self.XAI_GROK_URL
            self.model_name = model_name or "grok-2-latest"
            self.provider_label = "xAI Grok"

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        if not self.is_available():
            raise LLMProviderError("API key is not configured or missing in .env.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.2,
        }

        last_error = ""

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=45,
                )

                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if not choices:
                        raise LLMProviderError(f"{self.provider_label} response contained no completion choices.")
                    content = choices[0].get("message", {}).get("content", "")
                    if not content:
                        raise LLMProviderError(f"{self.provider_label} returned empty completion content.")
                    return content.strip()

                # Parse non-200 responses
                err_detail = "Unknown error"
                try:
                    err_json = response.json()
                    err_detail = err_json.get("error", {}).get("message") if isinstance(err_json.get("error"), dict) else err_json.get("error") or response.text
                except Exception:
                    err_detail = response.text

                # Auth errors (401 unauthorized or 400 invalid argument) fail immediately without useless retries
                if response.status_code in (400, 401) and any(kw in str(err_detail).lower() for kw in ["api key", "unauthorized", "invalid_api_key", "authentication"]):
                    raise LLMProviderError(
                        f"Authentication failed on {self.provider_label}: {err_detail}. "
                        f"Please check your API key in .env."
                    )

                # Transient errors (429 rate limit, 500/502/503 server error) -> retry
                last_error = f"HTTP {response.status_code}: {err_detail}"
                logger.warning(f"{self.provider_label} attempt {attempt}/{self.max_retries} failed: {last_error}")

                if attempt < self.max_retries:
                    wait_time = 2 * attempt
                    logger.info(f"Retrying {self.provider_label} in {wait_time}s...")
                    time.sleep(wait_time)

            except requests.exceptions.Timeout:
                last_error = "Connection timed out after 45 seconds"
                logger.warning(f"{self.provider_label} attempt {attempt}/{self.max_retries} timed out.")
                if attempt < self.max_retries:
                    time.sleep(2 * attempt)

            except requests.exceptions.RequestException as re:
                last_error = f"Network connection error: {str(re)}"
                logger.warning(f"{self.provider_label} attempt {attempt}/{self.max_retries} network error: {re}")
                if attempt < self.max_retries:
                    time.sleep(2 * attempt)

            except Exception as e:
                if isinstance(e, LLMProviderError):
                    raise
                last_error = f"Unexpected error: {str(e)}"
                logger.warning(f"{self.provider_label} attempt {attempt}/{self.max_retries} unexpected error: {e}")
                if attempt < self.max_retries:
                    time.sleep(2 * attempt)

        # All retries failed -> return clear failure message, NEVER hardcode
        raise LLMProviderError(
            f"{self.provider_label} request failed after {self.max_retries} attempts. Last error: {last_error}"
        )
