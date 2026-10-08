"""
Abstract Interfaces and Protocols for the AI Coding Agent.
Ensures Interface Segregation (ISP) and Dependency Inversion (DIP).
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from core.models import (
    FileASTSummary,
    RelevanceResult,
    ImplementationPlan,
    CodePatchResult,
    TestExecutionResult,
)


class ILLMProvider(ABC):
    """Abstraction for Large Language Model communication."""

    @abstractmethod
    def generate_completion(self, prompt: str, system_instruction: str = "") -> str:
        """Generate response given a prompt and optional system instructions."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is properly configured and reachable."""
        pass


class ICodebaseInspector(ABC):
    """Abstraction for reading and syntactic analysis of source codebases."""

    @abstractmethod
    def scan_codebase(self, root_dir: str) -> Dict[str, str]:
        """Scan directory and return mapping of relative filepath -> file content."""
        pass

    @abstractmethod
    def analyze_ast(self, file_map: Dict[str, str]) -> List[FileASTSummary]:
        """Parse source files into structural summaries (classes, functions, imports)."""
        pass


class IRelevanceAnalyzer(ABC):
    """Abstraction for identifying relevant files based on user intent."""

    @abstractmethod
    def identify_relevant_files(
        self,
        task_prompt: str,
        file_map: Dict[str, str],
        ast_summaries: List[FileASTSummary],
    ) -> RelevanceResult:
        """Determine which files are critical to fulfilling the user prompt."""
        pass


class IPlanGenerator(ABC):
    """Abstraction for decomposing a coding request into a verified step-by-step plan."""

    @abstractmethod
    def create_plan(
        self,
        task_prompt: str,
        relevant_files: List[str],
        file_map: Dict[str, str],
        reasoning: str,
    ) -> ImplementationPlan:
        """Generate architectural implementation plan."""
        pass


class ICodePatcher(ABC):
    """Abstraction for generating modifications and unified diffs."""

    @abstractmethod
    def generate_patch(
        self,
        task_prompt: str,
        plan: ImplementationPlan,
        file_map: Dict[str, str],
    ) -> CodePatchResult:
        """Generate modified file contents, diffs, and change explanations."""
        pass


class ICodeValidator(ABC):
    """Abstraction for executing validation test suites and syntax checks."""

    @abstractmethod
    def validate(
        self,
        original_codebase_dir: str,
        modified_files: Dict[str, str],
    ) -> TestExecutionResult:
        """Run tests against the modified codebase in an isolated environment."""
        pass
