"""
GitHub Repository Loader Service.
Enables cloning external public repositories for the AI Coding Agent to inspect and modify.
Follows Single Responsibility Principle (SRP).
"""
import os
import shutil
import subprocess
import logging
from typing import Tuple

logger = logging.getLogger("RepoLoader")


class GitHubRepoLoader:
    """Clones and manages GitHub repositories in a dedicated local workspace directory."""

    def __init__(self, base_storage_dir: str):
        self.base_dir = os.path.abspath(base_storage_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def clone_repository(self, repo_url: str) -> Tuple[bool, str, str]:
        """
        Clones a repository using shallow clone (--depth 1).
        Returns (success: bool, target_directory: str, message: str).
        """
        clean_url = repo_url.strip()
        if not clean_url:
            return False, "", "Empty repository URL provided."

        if not (clean_url.startswith("https://github.com/") or clean_url.endswith(".git")):
            return False, "", "Invalid URL format. Please provide a valid GitHub repository URL."

        # Extract repo name from URL (e.g. username/my-repo -> my-repo)
        repo_name = clean_url.rstrip("/").split("/")[-1].replace(".git", "")
        if not repo_name:
            repo_name = "cloned_repo"

        target_dir = os.path.join(self.base_dir, repo_name)

        # If repo exists, clean it up or use existing
        if os.path.exists(target_dir):
            try:
                shutil.rmtree(target_dir, ignore_errors=True)
            except Exception as e:
                logger.warning(f"Could not remove existing directory {target_dir}: {e}")

        try:
            cmd = ["git", "clone", "--depth", "1", clean_url, target_dir]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                err_msg = result.stderr.strip() or result.stdout.strip() or "Unknown git error"
                return False, "", f"Failed to clone repository: {err_msg}"

            # Verify that repository contains source files
            has_py_files = False
            for _, _, files in os.walk(target_dir):
                if any(f.endswith(".py") for f in files):
                    has_py_files = True
                    break

            if not has_py_files:
                return False, target_dir, f"Cloned '{repo_name}' successfully, but found no .py source files."

            return True, target_dir, f"Successfully cloned repository: {repo_name}"

        except subprocess.TimeoutExpired:
            return False, "", "Git clone operation timed out after 60 seconds."
        except Exception as e:
            logger.error(f"Error during repository clone: {e}")
            return False, "", f"Git clone failed: {str(e)}"
