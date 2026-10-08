"""
Domain Data Transfer Objects (DTOs) and Entities.
Follows clean architecture with strongly-typed dataclasses.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class WorkflowStep(str, Enum):
    IDLE = "IDLE"
    UNDERSTAND_TASK = "UNDERSTAND_TASK"
    INSPECT_CODEBASE = "INSPECT_CODEBASE"
    IDENTIFY_FILES = "IDENTIFY_FILES"
    GENERATE_PLAN = "GENERATE_PLAN"
    PROPOSE_CHANGES = "PROPOSE_CHANGES"
    VALIDATE_CHANGES = "VALIDATE_CHANGES"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class FileASTSummary:
    """Summary of syntactic structures inside a source file."""
    filepath: str
    classes: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    imports: List[str] = field(default_factory=list)
    line_count: int = 0


@dataclass(frozen=True)
class RelevanceResult:
    """Result of relevant file identification."""
    selected_files: List[str]
    reasoning: str
    confidence_score: float = 1.0


@dataclass(frozen=True)
class ImplementationPlan:
    """Implementation plan produced by the planner."""
    task_intent: str
    markdown_plan: str
    target_files: List[str]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class CodePatchResult:
    """Result of code modification step."""
    modified_files: Dict[str, str]  # filepath -> full updated content
    diffs: Dict[str, str]           # filepath -> unified diff string
    explanation: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass(frozen=True)
class TestExecutionResult:
    """Result of running validation suite against modified code."""
    passed: bool
    total_tests: int
    passed_tests: int
    failed_tests: int
    output_log: str
    duration_seconds: float
    error_summary: Optional[str] = None


@dataclass
class WorkflowState:
    """Comprehensive state tracking object for the entire agent pipeline."""
    task_prompt: str
    codebase_path: str
    current_step: WorkflowStep = WorkflowStep.IDLE
    file_map: Dict[str, str] = field(default_factory=dict)
    ast_summaries: List[FileASTSummary] = field(default_factory=list)
    relevance_result: Optional[RelevanceResult] = None
    plan: Optional[ImplementationPlan] = None
    patch_result: Optional[CodePatchResult] = None
    validation_result: Optional[TestExecutionResult] = None
    error_message: Optional[str] = None
    logs: List[str] = field(default_factory=list)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def add_log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")
