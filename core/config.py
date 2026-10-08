"""
Configuration management for the AI Coding Agent.
Handles environment variables and application runtime settings cleanly.
Auto-detects model between Groq Cloud and xAI Grok.
"""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration."""
    grok_api_key: str = (os.getenv("GROK_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY") or "").strip()
    default_timeout_seconds: int = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "30"))
    sandbox_temp_dir: Optional[str] = os.getenv("SANDBOX_TEMP_DIR", None)
    app_version: str = "1.0.0"

    @property
    def grok_model(self) -> str:
        explicit = os.getenv("GROK_MODEL") or os.getenv("GROQ_MODEL")
        if explicit:
            return explicit
        if self.grok_api_key.startswith("gsk_"):
            return "openai/gpt-oss-120b"
        return "grok-2-latest"

    @property
    def has_api_key(self) -> bool:
        return bool(self.grok_api_key and len(self.grok_api_key.strip()) > 5)

    @property
    def provider_display(self) -> str:
        if self.grok_api_key.startswith("gsk_"):
            return "Groq Cloud (LPU)"
        return "xAI Grok"


def get_config() -> AppConfig:
    """Factory method for accessing application configuration."""
    return AppConfig()
