"""
Base abstract class for LLM providers.
Enforces the Open/Closed Principle (OCP) and Liskov Substitution Principle (LSP).
"""
from abc import ABC, abstractmethod
from core.interfaces import ILLMProvider


class BaseLLMProvider(ILLMProvider, ABC):
    """Abstract base class that all concrete LLM providers must implement."""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    @abstractmethod
    def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        """Subclasses implement API or mock specific generation logic."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is operational."""
        pass
