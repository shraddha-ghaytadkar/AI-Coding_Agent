"""
Custom Domain Exceptions for AI Coding Agent.
Provides structured error hierarchy for precise handling and telemetry.
"""


class AgentBaseException(Exception):
    """Base exception for all agent-related domain errors."""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class CodebaseInspectionError(AgentBaseException):
    """Raised when codebase discovery or AST parsing fails."""
    pass


class RelevanceAnalysisError(AgentBaseException):
    """Raised when relevant file identification fails."""
    pass


class PlanningError(AgentBaseException):
    """Raised when plan generation fails."""
    pass


class CodeGenerationError(AgentBaseException):
    """Raised when code generation or patch synthesis fails."""
    pass


class ValidationError(AgentBaseException):
    """Raised when test execution or sandbox validation encounters an internal error."""
    pass


class LLMProviderError(AgentBaseException):
    """Raised when an external LLM API call fails."""
    pass
