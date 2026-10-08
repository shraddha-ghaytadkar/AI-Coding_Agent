"""
Codebase Inspector implementation.
Follows Single Responsibility Principle (SRP) by focusing strictly on filesystem scanning and AST analysis.
"""
import ast
import os
import logging
from typing import Dict, List
from core.exceptions import CodebaseInspectionError
from core.interfaces import ICodebaseInspector
from core.models import FileASTSummary

logger = logging.getLogger("CodebaseInspector")


class CodebaseInspector(ICodebaseInspector):
    """Concrete implementation of codebase discovery and syntactic AST extraction."""

    def scan_codebase(self, root_dir: str) -> Dict[str, str]:
        """Recursively scan a directory and load all Python files into memory."""
        abs_root = os.path.abspath(root_dir)
        if not os.path.exists(abs_root) or not os.path.isdir(abs_root):
            raise CodebaseInspectionError(f"Target directory does not exist or is not a directory: {abs_root}")

        file_map: Dict[str, str] = {}
        try:
            for dirpath, _, filenames in os.walk(abs_root):
                for filename in filenames:
                    if filename.endswith(".py") and not filename.startswith("."):
                        file_path = os.path.join(dirpath, filename)
                        rel_path = os.path.relpath(file_path, abs_root).replace("\\", "/")
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                file_map[rel_path] = f.read()
                        except Exception as e:
                            logger.warning(f"Failed to read file {file_path}: {e}")
                            file_map[rel_path] = f"# Error reading file: {e}"

            if not file_map:
                raise CodebaseInspectionError(f"No Python source files discovered in: {abs_root}")

            return file_map

        except Exception as e:
            if isinstance(e, CodebaseInspectionError):
                raise
            raise CodebaseInspectionError(f"Failed scanning codebase at {abs_root}: {str(e)}") from e

    def analyze_ast(self, file_map: Dict[str, str]) -> List[FileASTSummary]:
        """Extract top-level classes, functions, and imports using Python AST."""
        summaries: List[FileASTSummary] = []

        for rel_path, content in file_map.items():
            classes: List[str] = []
            functions: List[str] = []
            imports: List[str] = []

            try:
                tree = ast.parse(content, filename=rel_path)
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.ClassDef):
                        classes.append(node.name)
                        for item in node.body:
                            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                functions.append(f"{node.name}.{item.name}")
                                functions.append(item.name)
                    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        functions.append(node.name)
                    elif isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ""
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}")

            except SyntaxError as se:
                logger.warning(f"Syntax error parsing AST for {rel_path}: {se}")
            except Exception as e:
                logger.warning(f"AST extraction error for {rel_path}: {e}")

            line_count = len(content.splitlines())
            summaries.append(
                FileASTSummary(
                    filepath=rel_path,
                    classes=classes,
                    functions=functions,
                    imports=imports,
                    line_count=line_count,
                )
            )

        return summaries
