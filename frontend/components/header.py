"""
Header component for the web interface.
"""
import streamlit as st


def render_header():
    """Renders the top branding header."""
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">Autonomous AI Coding Agent</div>
            <div class="main-subtitle">
                Natural Language Reasoning • Codebase AST Inspection • Planning • Patch Synthesis • Sandbox Validation
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
