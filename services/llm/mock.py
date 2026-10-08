"""
Mock LLM Provider for unit testing and offline pipeline verification.
Dynamically responds to prompts based on input context without static domain hardcoding.
"""
import json
import logging
import re
from services.llm.base import BaseLLMProvider

logger = logging.getLogger("MockLLMProvider")


class MockLLMProvider(BaseLLMProvider):
    """Provides dynamic simulated responses for test execution when Gemini API key is absent."""

    def __init__(self):
        super().__init__(provider_name="Mock/Test")

    def is_available(self) -> bool:
        return True

    def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        prompt_lower = prompt.lower()

        # 1. Code Generation (Specific to Coder prompt)
        if "target files and their complete existing code" in prompt_lower or "generate the complete updated code" in prompt_lower:
            files_match = re.search(r"TARGET FILES AND THEIR COMPLETE EXISTING CODE:\s*(\{[\s\S]*?\})\s*CRITICAL INSTRUCTIONS:", prompt)
            modified_files = {}
            if files_match:
                try:
                    files_dict = json.loads(files_match.group(1))
                    for fname, code in files_dict.items():
                        # Append non-breaking valid comment
                        modified_files[fname] = code + "\n# Dynamically verified by AI Agent\n"
                except Exception:
                    pass

            if not modified_files:
                modified_files = {"service.py": "# Dynamic modification\n"}

            return json.dumps({
                "modified_files": modified_files,
                "explanation": "Dynamically updated source code to satisfy specifications."
            })

        # 2. File Relevance Identification
        if "available files:" in prompt_lower or "directly relevant" in prompt_lower:
            available_match = re.search(r"available files:\s*(\[[^\]]+\])", prompt, re.IGNORECASE)
            available = []
            if available_match:
                try:
                    available = json.loads(available_match.group(1).replace("'", '"'))
                except Exception:
                    pass

            candidates = [f for f in available if not f.startswith("test_")] or available[:1]
            return json.dumps({
                "relevant_files": candidates[:2] if len(candidates) >= 2 else candidates,
                "reasoning": "Identified source files matching the target domain operations."
            })

        # 3. Plan Generation
        if "principal software architect" in prompt_lower or "implementation plan" in prompt_lower:
            return """### Dynamic Implementation Plan
1. **Analyze Requirements**: Parse the coding task and determine impacted modules.
2. **Implement Modifications**: Apply clean, backward-compatible logic to the target source files.
3. **Validation**: Execute automated unit tests in the sandbox to ensure regression-free behavior.
"""

        return "Completed generation."
