"""
Code Viewer Component.
Displays the file selected from the sidebar file explorer with syntax highlighting and file metadata.
Clean design without emojis.
"""
import os
import streamlit as st
from services.inspector import CodebaseInspector


def render_code_viewer(codebase_dir: str, active_file: str = None):
    """Renders a code viewer for the currently active file."""
    if not codebase_dir or not os.path.exists(codebase_dir):
        st.info("No codebase loaded. Select a project or clone a GitHub repository.")
        return

    inspector = CodebaseInspector()
    try:
        file_map = inspector.scan_codebase(codebase_dir)
        ast_summaries = inspector.analyze_ast(file_map)
    except Exception as e:
        st.warning(f"Could not load files from codebase: {e}")
        return

    if not file_map:
        st.info("No Python source files discovered in this codebase.")
        return

    # Determine which file to display
    available_files = list(file_map.keys())
    target_file = active_file if active_file in available_files else available_files[0]

    # Find AST summary for this file
    summary = next((s for s in ast_summaries if s.filepath == target_file), None)

    # Clean tab bar header
    st.markdown(
        f"""
        <div style="background-color: #1e1e2e; border: 1px solid #313244; border-bottom: none; border-radius: 8px 8px 0 0; padding: 8px 16px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-family: monospace; font-weight: 600; color: #cdd6f4;">{target_file}</span>
            </div>
            <div style="font-size: 0.8rem; color: #a6adc8;">
                {len(file_map[target_file].splitlines())} lines
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if summary:
        classes_str = ", ".join(summary.classes) or "None"
        funcs_str = ", ".join(summary.functions[:6]) or "None"
        st.caption(f"Symbols: Classes: `{classes_str}` | Functions/Methods: `{funcs_str}`")

    # Code Display
    st.code(file_map[target_file], language="python")
