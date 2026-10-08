"""
Implementation Planner implementation.
Generates structured Markdown plans before executing modifications.
Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
"""
import logging
from typing import Dict, List
from core.exceptions import PlanningError
from core.interfaces import IPlanGenerator, ILLMProvider
from core.models import ImplementationPlan

logger = logging.getLogger("ImplementationPlanner")


class ImplementationPlanner(IPlanGenerator):
    """Produces detailed engineering blueprints for code alterations."""

    def __init__(self, llm_provider: ILLMProvider):
        self.llm_provider = llm_provider

    def create_plan(
        self,
        task_prompt: str,
        relevant_files: List[str],
        file_map: Dict[str, str],
        reasoning: str,
    ) -> ImplementationPlan:
        if not relevant_files:
            raise PlanningError("Cannot create implementation plan without relevant target files.")

        # Build context of the files that will be modified
        file_snippets = []
        for fname in relevant_files:
            content = file_map.get(fname, "")
            file_snippets.append(f"### File: `{fname}`\n```python\n{content}\n```")

        context_code = "\n\n".join(file_snippets)

        prompt = f"""You are a Principal Software Architect.
Produce a comprehensive, step-by-step implementation plan for the following engineering request.

USER CODING REQUEST:
\"{task_prompt}\"

RELEVANT FILES IDENTIFIED:
{relevant_files}

SELECTION RATIONALE:
{reasoning}

TARGET CODE CONTEXT:
{context_code}

INSTRUCTIONS:
Generate a well-organized markdown plan covering:
1. **Executive Summary**: Core goal of the change.
2. **Architecture & Design**: Key design patterns and data structures impacted.
3. **Target Modifications by File**:
   - For each relevant file, specify exact methods or classes to modify, add, or refactor.
4. **Edge Cases & Input Validation**: Null checks, boundary conditions, error handling.
5. **Testing & Validation Strategy**: How the changes will be validated by existing and new tests.

Output ONLY the markdown implementation plan.
"""

        try:
            markdown_plan = self.llm_provider.generate_completion(
                prompt=prompt,
                system_instruction="You are a Principal Software Architect. Return clean, authoritative markdown."
            )
            return ImplementationPlan(
                task_intent=task_prompt,
                markdown_plan=markdown_plan.strip(),
                target_files=relevant_files,
            )
        except Exception as e:
            logger.error(f"Planning step encountered an error: {e}")
            raise PlanningError(f"Failed to generate implementation plan: {str(e)}") from e
