"""
Workflow Orchestration State Machine.
Coordinates the end-to-end 7-step coding-agent lifecycle.
Follows Dependency Inversion Principle (DIP) and Single Responsibility Principle (SRP).
"""
import logging
from datetime import datetime
from typing import Callable, Optional
from core.interfaces import (
    ICodebaseInspector,
    IRelevanceAnalyzer,
    IPlanGenerator,
    ICodePatcher,
    ICodeValidator,
)
from core.models import WorkflowState, WorkflowStep

logger = logging.getLogger("AgentWorkflowOrchestrator")

StepCallback = Callable[[WorkflowStep, str], None]


class AgentWorkflowOrchestrator:
    """Coordinates the end-to-end coding agent execution lifecycle."""

    def __init__(
        self,
        inspector: ICodebaseInspector,
        relevance_analyzer: IRelevanceAnalyzer,
        plan_generator: IPlanGenerator,
        code_patcher: ICodePatcher,
        validator: ICodeValidator,
        on_step_change: Optional[StepCallback] = None,
    ):
        self.inspector = inspector
        self.relevance_analyzer = relevance_analyzer
        self.plan_generator = plan_generator
        self.code_patcher = code_patcher
        self.validator = validator
        self.on_step_change = on_step_change

    def execute(self, task_prompt: str, codebase_path: str) -> WorkflowState:
        """Executes the full pipeline sequentially with robust telemetry and error boundaries."""
        state = WorkflowState(task_prompt=task_prompt, codebase_path=codebase_path)
        state.add_log(f"Starting coding agent workflow for task: '{task_prompt[:60]}...'")

        try:
            # Step 1: Understand Task
            self._notify(state, WorkflowStep.UNDERSTAND_TASK, "Analyzing task requirements and intent...")

            # Step 2: Inspect Codebase
            self._notify(state, WorkflowStep.INSPECT_CODEBASE, "Scanning codebase and parsing AST structures...")
            state.file_map = self.inspector.scan_codebase(codebase_path)
            state.ast_summaries = self.inspector.analyze_ast(state.file_map)
            state.add_log(f"Scanned {len(state.file_map)} files; extracted {len(state.ast_summaries)} AST summaries.")

            # Step 3: Identify Relevant Files
            self._notify(state, WorkflowStep.IDENTIFY_FILES, "Identifying relevant files for the requested change...")
            state.relevance_result = self.relevance_analyzer.identify_relevant_files(
                task_prompt=task_prompt,
                file_map=state.file_map,
                ast_summaries=state.ast_summaries,
            )
            state.add_log(f"Selected relevant files: {state.relevance_result.selected_files}")

            # Step 4: Generate Implementation Plan
            self._notify(state, WorkflowStep.GENERATE_PLAN, "Generating step-by-step architectural plan...")
            state.plan = self.plan_generator.create_plan(
                task_prompt=task_prompt,
                relevant_files=state.relevance_result.selected_files,
                file_map=state.file_map,
                reasoning=state.relevance_result.reasoning,
            )
            state.add_log("Implementation plan generated successfully.")

            # Step 5 & 6: Propose Changes & Generate Diff
            self._notify(state, WorkflowStep.PROPOSE_CHANGES, "Synthesizing code changes and unified diffs...")
            state.patch_result = self.code_patcher.generate_patch(
                task_prompt=task_prompt,
                plan=state.plan,
                file_map=state.file_map,
            )
            state.add_log(f"Synthesized patches for {len(state.patch_result.modified_files)} file(s).")

            # Step 7: Validate Changes in Sandbox
            self._notify(state, WorkflowStep.VALIDATE_CHANGES, "Running automated test suite in sandbox...")
            state.validation_result = self.validator.validate(
                original_codebase_dir=codebase_path,
                modified_files=state.patch_result.modified_files,
            )
            state.add_log(
                f"Validation finished. Result: {'PASSED' if state.validation_result.passed else 'FAILED'} "
                f"({state.validation_result.passed_tests}/{state.validation_result.total_tests} passed in {state.validation_result.duration_seconds}s)"
            )

            # Completion
            self._notify(state, WorkflowStep.COMPLETED, "Workflow completed successfully.")
            state.completed_at = datetime.now()
            return state

        except Exception as e:
            logger.error(f"Workflow execution failure at step {state.current_step}: {e}")
            state.current_step = WorkflowStep.FAILED
            state.error_message = str(e)
            state.add_log(f"ERROR: {str(e)}")
            state.completed_at = datetime.now()
            if self.on_step_change:
                self.on_step_change(WorkflowStep.FAILED, f"Failed: {str(e)}")
            return state

    def _notify(self, state: WorkflowState, step: WorkflowStep, message: str) -> None:
        state.current_step = step
        state.add_log(message)
        if self.on_step_change:
            self.on_step_change(step, message)
