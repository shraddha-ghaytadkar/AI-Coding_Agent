"""
Code Modification and Patching Engine.
Synthesizes modified source files dynamically via LLM and produces unified diffs with AST syntax verification.
Strictly dynamic: NO hardcoded templates or fallbacks.
Follows Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).
"""
import ast
import difflib
import json
import logging
import re
from typing import Dict, List, Tuple
from core.exceptions import CodeGenerationError
from core.interfaces import ICodePatcher, ILLMProvider
from core.models import CodePatchResult, ImplementationPlan

logger = logging.getLogger("CodeModificationEngine")


class CodeModificationEngine(ICodePatcher):
    """Generates precise, dynamic code alterations and unified diffs using LLM reasoning."""

    def __init__(self, llm_provider: ILLMProvider):
        self.llm_provider = llm_provider

    def generate_patch(
        self,
        task_prompt: str,
        plan: ImplementationPlan,
        file_map: Dict[str, str],
    ) -> CodePatchResult:
        target_files = plan.target_files
        if not target_files:
            raise CodeGenerationError("No target files identified for patching.")

        # Extract current contents of files to modify
        target_context = {
            fname: file_map.get(fname, "") for fname in target_files if fname in file_map
        }

        prompt = f"""You are an autonomous AI Software Engineer.
Your task is to implement the requested changes dynamically according to the user request and implementation plan.

USER REQUEST:
\"{task_prompt}\"

ARCHITECTURAL PLAN:
{plan.markdown_plan}

TARGET FILES AND THEIR COMPLETE EXISTING CODE:
{json.dumps(target_context, indent=2)}

CRITICAL INSTRUCTIONS:
1. Generate the COMPLETE updated code for each target file. Do NOT truncate with '...' or omit existing functions.
2. Ensure valid Python syntax with correct imports and indentation.
3. Preserve existing methods while adding/modifying the requested functionality.
4. You MUST respond with a valid JSON object in the exact format:
{{
    "modified_files": {{
        "filename.py": "complete updated code as a string"
    }},
    "explanation": "Detailed explanation of what code was modified, added, or refactored and why."
}}
Return ONLY the JSON object.
"""

        try:
            raw_response = self.llm_provider.generate_completion(
                prompt=prompt,
                system_instruction="You are an expert autonomous software engineer. Return only valid JSON with complete updated Python source code."
            )

            modified_files, explanation = self._parse_llm_code_response(
                raw_response, target_context
            )

            if not modified_files:
                raise CodeGenerationError("LLM did not produce any modified source files.")

            # Validate Python syntax of all generated files
            self._verify_syntax(modified_files)

            # Generate unified diffs
            diffs = self._generate_diffs(file_map, modified_files)

            return CodePatchResult(
                modified_files=modified_files,
                diffs=diffs,
                explanation=explanation,
            )

        except Exception as e:
            if isinstance(e, CodeGenerationError):
                raise
            logger.error(f"Dynamic patch generation failed: {e}")
            raise CodeGenerationError(f"Failed to generate code patch dynamically: {str(e)}") from e

    def _parse_llm_code_response(
        self, raw_text: str, target_context: Dict[str, str]
    ) -> Tuple[Dict[str, str], str]:
        """
        Parses LLM output dynamically using JSON extraction, with regex fallback for markdown code fences.
        Does NOT use any hardcoded code strings.
        """
        cleaned = raw_text.strip()

        # Remove markdown wrapper if present
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[1]
            if cleaned.endswith("```"):
                cleaned = cleaned.rsplit("```", 1)[0]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:].strip()

        # Strategy 1: Parse JSON directly
        try:
            data = json.loads(cleaned)
            modified_files = data.get("modified_files", {})
            explanation = data.get("explanation", "Code updated based on user request.")
            if isinstance(modified_files, dict) and modified_files:
                return modified_files, explanation
        except Exception:
            pass

        # Strategy 2: Search for embedded JSON object in response
        json_match = re.search(r'\{[\s\S]*"modified_files"[\s\S]*\}', raw_text)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                modified_files = data.get("modified_files", {})
                explanation = data.get("explanation", "Code updated dynamically.")
                if isinstance(modified_files, dict) and modified_files:
                    return modified_files, explanation
            except Exception:
                pass

        # Strategy 3: Multi-file code fence parsing (```python ... ``` with filename comment)
        parsed_files = {}
        file_pattern = re.findall(r'```(?:python)?\s*(?:#\s*file:\s*(\S+)|#\s*filename:\s*(\S+))?\n([\s\S]*?)```', raw_text)
        for match in file_pattern:
            fname = match[0] or match[1]
            code = match[2].strip()
            if fname and fname in target_context:
                parsed_files[fname] = code
            elif len(target_context) == 1:
                # If only one file was targeted, assign code to that file
                single_fname = list(target_context.keys())[0]
                parsed_files[single_fname] = code

        if parsed_files:
            return parsed_files, "Extracted updated code from model code fences."

        raise CodeGenerationError(
            f"Could not parse valid code from LLM output. Model response:\n{raw_text[:300]}..."
        )

    def _verify_syntax(self, modified_files: Dict[str, str]) -> None:
        """Verifies that all generated code is valid Python syntax."""
        for filename, code in modified_files.items():
            try:
                ast.parse(code, filename=filename)
            except SyntaxError as se:
                logger.error(f"Syntax error in generated code for {filename}: {se}")
                raise CodeGenerationError(
                    f"Syntax error in model-generated code for '{filename}' at line {se.lineno}: {se.msg}"
                ) from se

    def _generate_diffs(
        self, original_map: Dict[str, str], modified_files: Dict[str, str]
    ) -> Dict[str, str]:
        """Computes true unified diffs between original and newly generated code."""
        diffs = {}
        for fname, new_code in modified_files.items():
            old_code = original_map.get(fname, "")
            diff_lines = list(difflib.unified_diff(
                old_code.splitlines(keepends=True),
                new_code.splitlines(keepends=True),
                fromfile=f"a/{fname}",
                tofile=f"b/{fname}",
            ))
            diffs[fname] = "".join(diff_lines) or f"# No modifications made to {fname}"
        return diffs
