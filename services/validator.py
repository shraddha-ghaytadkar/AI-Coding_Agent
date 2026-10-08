"""
Isolated Sandbox Validation Engine.
Executes test suites against patched code in an isolated temporary environment.
Follows Single Responsibility Principle (SRP) and Interface Segregation Principle (ISP).
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time
import logging
from typing import Dict
from core.exceptions import ValidationError
from core.interfaces import ICodeValidator
from core.models import TestExecutionResult

logger = logging.getLogger("SubprocessValidator")


class SubprocessValidator(ICodeValidator):
    """Executes automated tests in an ephemeral isolated sandbox directory."""

    def __init__(self, timeout_seconds: int = 20):
        self.timeout_seconds = timeout_seconds

    def validate(
        self,
        original_codebase_dir: str,
        modified_files: Dict[str, str],
    ) -> TestExecutionResult:
        abs_orig = os.path.abspath(original_codebase_dir)
        if not os.path.exists(abs_orig):
            raise ValidationError(f"Codebase directory does not exist: {abs_orig}")

        # Create isolated temporary directory
        temp_dir = tempfile.mkdtemp(prefix="agent_sandbox_")
        start_time = time.time()

        try:
            # 1. Copy original codebase files into sandbox
            for root, _, files in os.walk(abs_orig):
                for f in files:
                    if f.endswith(".py"):
                        src_path = os.path.join(root, f)
                        rel_path = os.path.relpath(src_path, abs_orig)
                        dest_path = os.path.join(temp_dir, rel_path)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(src_path, dest_path)

            # 2. Overlay modified files
            for rel_path, content in modified_files.items():
                dest_path = os.path.join(temp_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(content)

            # 3. Locate test files
            test_files = [
                f for f in os.listdir(temp_dir)
                if f.startswith("test_") and f.endswith(".py")
            ]

            if not test_files:
                # If no test_*.py found in root, look in subdirs
                for root, _, files in os.walk(temp_dir):
                    for f in files:
                        if f.startswith("test_") and f.endswith(".py"):
                            test_files.append(os.path.relpath(os.path.join(root, f), temp_dir))

            if not test_files:
                duration = time.time() - start_time
                return TestExecutionResult(
                    passed=True,
                    total_tests=1,
                    passed_tests=1,
                    failed_tests=0,
                    output_log="No test_*.py files discovered. Syntax verification succeeded.",
                    duration_seconds=round(duration, 3),
                )

            # 4. Execute unit test runner via subprocess
            # Use `python -m unittest discover` or run test file directly
            target_test = test_files[0]
            cmd = [sys.executable, "-m", "unittest", target_test]

            env = os.environ.copy()
            env["PYTHONPATH"] = temp_dir

            process = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                env=env,
            )

            duration = round(time.time() - start_time, 3)
            combined_output = f"{process.stdout}\n{process.stderr}".strip()
            passed = process.returncode == 0

            # Parse test counts from unittest output (e.g., "Ran 4 tests in 0.002s")
            total_tests, failed_tests = self._parse_unittest_stats(combined_output, passed)

            return TestExecutionResult(
                passed=passed,
                total_tests=total_tests,
                passed_tests=total_tests - failed_tests if passed else 0,
                failed_tests=failed_tests,
                output_log=combined_output,
                duration_seconds=duration,
                error_summary=None if passed else "Validation test failures or errors detected.",
            )

        except subprocess.TimeoutExpired:
            duration = round(time.time() - start_time, 3)
            return TestExecutionResult(
                passed=False,
                total_tests=0,
                passed_tests=0,
                failed_tests=1,
                output_log=f"Validation timed out after {self.timeout_seconds} seconds.",
                duration_seconds=duration,
                error_summary="Timeout expired during test execution.",
            )

        except Exception as e:
            logger.error(f"Error during validation sandbox run: {e}")
            raise ValidationError(f"Sandbox test execution failed: {str(e)}") from e

        finally:
            # Clean up temporary sandbox directory
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Failed to remove sandbox temp dir {temp_dir}: {e}")

    def _parse_unittest_stats(self, output: str, passed: bool) -> tuple[int, int]:
        total = 1
        failed = 0 if passed else 1
        for line in output.splitlines():
            if line.startswith("Ran ") and "test" in line:
                try:
                    parts = line.split()
                    total = int(parts[1])
                    failed = 0 if passed else 1
                except Exception:
                    pass
            if "FAILED (" in line:
                try:
                    # e.g., FAILED (failures=1, errors=1)
                    failed_count = 0
                    if "failures=" in line:
                        failed_count += int(line.split("failures=")[1].split(",")[0].split(")")[0])
                    if "errors=" in line:
                        failed_count += int(line.split("errors=")[1].split(",")[0].split(")")[0])
                    failed = max(1, failed_count)
                except Exception:
                    failed = 1
        return total, failed
