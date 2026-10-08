"""
AI Coding Agent Application Entry Point.
Delegates presentation logic to the frontend package.
Follows Clean Architecture and separation of concerns.
"""
import os
import sys

# Ensure workspace root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from frontend.dashboard import render_app

if __name__ == "__main__":
    render_app(base_dir=BASE_DIR)
