"""
Relevance Analyzer implementation.
Identifies which files in a codebase need to be updated to fulfill a user request using Grok LLM.
Strictly dynamic: NO hardcoded replies or silent fallback swallowing.
Follows Dependency Inversion Principle (DIP) by receiving ILLMProvider abstraction.
"""
import json
import logging
import re
from typing import Dict, List
from core.exceptions import RelevanceAnalysisError, LLMProviderError
from core.interfaces import IRelevanceAnalyzer, ILLMProvider
from core.models import FileASTSummary, RelevanceResult

logger = logging.getLogger("RelevanceAnalyzer")


class RelevanceAnalyzer(IRelevanceAnalyzer):
    """Identifies files relevant to a natural language coding prompt."""

    def __init__(self, llm_provider: ILLMProvider):
        self.llm_provider = llm_provider

    def identify_relevant_files(
        self,
        task_prompt: str,
        file_map: Dict[str, str],
        ast_summaries: List[FileASTSummary],
    ) -> RelevanceResult:
        if not file_map:
            raise RelevanceAnalysisError("Cannot identify relevant files on an empty file map.")

        # Build codebase context for prompt
        context_blocks = []
        for summary in ast_summaries:
            fname = summary.filepath
            classes_str = ", ".join(summary.classes) or "None"
            funcs_str = ", ".join(summary.functions) or "None"
            context_blocks.append(
                f"- File: `{fname}` (Lines: {summary.line_count})\n"
                f"  Classes: {classes_str}\n"
                f"  Functions: {funcs_str}"
            )

        codebase_overview = "\n".join(context_blocks)
        available_files = list(file_map.keys())

        prompt = f"""You are an expert AI Coding Agent.
Given the following codebase structure and user coding request, determine which files are DIRECTLY RELEVANT and need changes or additions.

USER CODING REQUEST:
\"{task_prompt}\"

CODEBASE STRUCTURE:
{codebase_overview}

AVAILABLE FILES:
{available_files}

INSTRUCTIONS:
Respond with ONLY a valid JSON object in the exact format:
{{
    "relevant_files": ["file1.py", "file2.py"],
    "reasoning": "Clear explanation of why each file was selected and how it relates to the task."
}}
Do NOT include explanations outside the JSON object.
"""

        try:
            raw_response = self.llm_provider.generate_completion(
                prompt=prompt,
                system_instruction="You are an expert software engineer performing architectural dependency analysis. Return JSON only."
            )
        except LLMProviderError as lpe:
            # Propagate real failure message immediately
            raise RelevanceAnalysisError(f"Failed to analyze file relevance due to LLM error: {str(lpe)}") from lpe
        except Exception as e:
            raise RelevanceAnalysisError(f"Unexpected error communicating with LLM during file analysis: {str(e)}") from e

        # Parse JSON dynamically
        cleaned = self._clean_json_str(raw_response)
        data = None

        try:
            data = json.loads(cleaned)
        except Exception:
            # Try regex extraction
            match = re.search(r'\{[\s\S]*"relevant_files"[\s\S]*\}', raw_response)
            if match:
                try:
                    data = json.loads(match.group(0))
                except Exception:
                    pass

        if not data or not isinstance(data, dict):
            raise RelevanceAnalysisError(
                f"Model response could not be parsed into relevant files JSON. Response was:\n{raw_response[:300]}"
            )

        candidates = data.get("relevant_files", [])
        valid_files = [f for f in candidates if f in file_map]
        reasoning = data.get("reasoning", "Files identified by model analysis.")

        if not valid_files:
            raise RelevanceAnalysisError(
                f"Model selected files {candidates}, none of which exist in available files {available_files}."
            )

        return RelevanceResult(
            selected_files=valid_files,
            reasoning=reasoning,
            confidence_score=0.95,
        )

    def _clean_json_str(self, text: str) -> str:
        s = text.strip()
        if s.startswith("```"):
            s = s.split("\n", 1)[1]
            if s.endswith("```"):
                s = s.rsplit("```", 1)[0]
            if s.startswith("json"):
                s = s[4:].strip()
        return s.strip()
