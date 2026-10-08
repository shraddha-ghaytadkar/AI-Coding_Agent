"""
Main Dashboard view for the Streamlit Frontend.
Orchestrates header, sidebar explorer, top-level code viewer, and workflow results.
Clean presentation without emojis.
"""
import os
import streamlit as st
from core.config import get_config
from core.models import WorkflowStep
from orchestrator.factory import create_orchestrator
from frontend.styles import apply_custom_styles
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.workflow_view import render_workflow_results
from frontend.components.code_viewer import render_code_viewer


def render_app(base_dir: str):
    """Main rendering entrypoint for Streamlit web application."""
    # Apply custom design system and styles
    apply_custom_styles(st)

    # Initialize Session State
    if "workflow_state" not in st.session_state:
        st.session_state.workflow_state = None

    # Built-in sample codebases
    built_in_codebases = {
        "Task Tracker Service": {
            "dir": os.path.join(base_dir, "sample_codebases", "task_tracker"),
            "desc": "Multi-file task service with prioritization, status lifecycle, and unittest suite.",
            "sample_prompts": [
                "Add priority filtering method list_by_priority to TaskManager in service.py",
                "Add a method to bulk mark tasks as completed in service.py",
                "Add tag support to Task model and update TaskManager to filter by tag",
            ],
        },
        "Shopping Cart Calculator": {
            "dir": os.path.join(base_dir, "sample_codebases", "shopping_cart"),
            "desc": "E-commerce cart with item aggregation, coupons, tax calculation, and discounts.",
            "sample_prompts": [
                "Add get_grand_total method to ShoppingCart that computes final cost after discounts and tax",
                "Add seasonal summer discount coupon SUMMER25 (25% off) in discounts.py",
                "Add bulk discount logic when buying 5 or more items in cart.py",
            ],
        },
        "User Auth & Security": {
            "dir": os.path.join(base_dir, "sample_codebases", "user_auth"),
            "desc": "User authentication service with salted password hashing, lockout logic, and test coverage.",
            "sample_prompts": [
                "Add reset_failed_attempts method to Authenticator in authenticator.py to unlock user accounts",
                "Add email format validation during user registration in authenticator.py",
                "Add password change functionality verifying old password before hashing new password",
            ],
        },
    }

    # Render Sidebar (Explorer + GitHub Repo Loader + Cloned Repos)
    codebase_name, target_dir, active_file = render_sidebar(base_dir, built_in_codebases)

    # Render Header
    render_header()

    # Top Navigation Tabs: Agent Workflow & Code Viewer
    tab_agent, tab_viewer = st.tabs(
        ["Agent Workflow", "Code Viewer"]
    )

    with tab_agent:
        default_prompt = st.session_state.get(
            "current_prompt",
            built_in_codebases.get(codebase_name, {}).get("sample_prompts", [""])[0]
            if codebase_name in built_in_codebases else ""
        )

        task_input = st.text_area(
            "Enter Coding Task in Natural Language:",
            value=default_prompt,
            height=90,
            placeholder="e.g., Add priority filtering method list_by_priority to TaskManager in service.py",
        )

        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            run_clicked = st.button("Run Agent Pipeline", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("Clear Output", use_container_width=False):
                st.session_state.workflow_state = None
                st.rerun()

        if run_clicked:
            config = get_config()
            if not task_input.strip():
                st.warning("Please enter a coding task prompt.")
            elif not config.has_api_key:
                st.error(
                    "Configuration Notice: Please configure your API key in the backend .env file to run autonomous reasoning."
                )
            else:
                with st.spinner("Executing autonomous agent pipeline..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    def step_callback(step: WorkflowStep, msg: str):
                        status_text.text(f"Phase: {step.value} - {msg}")
                        pct_map = {
                            WorkflowStep.UNDERSTAND_TASK: 15,
                            WorkflowStep.INSPECT_CODEBASE: 30,
                            WorkflowStep.IDENTIFY_FILES: 45,
                            WorkflowStep.GENERATE_PLAN: 65,
                            WorkflowStep.PROPOSE_CHANGES: 85,
                            WorkflowStep.VALIDATE_CHANGES: 95,
                            WorkflowStep.COMPLETED: 100,
                            WorkflowStep.FAILED: 100,
                        }
                        progress_bar.progress(pct_map.get(step, 0))

                    orchestrator = create_orchestrator(
                        on_step_change=step_callback,
                    )

                    state = orchestrator.execute(
                        task_prompt=task_input.strip(),
                        codebase_path=target_dir,
                    )

                    st.session_state.workflow_state = state
                    progress_bar.progress(100)
                    status_text.empty()

        # Render Workflow Result Cards
        render_workflow_results(st.session_state.workflow_state)

    with tab_viewer:
        st.subheader("Source Code Viewer")
        st.caption(f"Viewing active file from: `{codebase_name}` (select files in the sidebar explorer)")
        render_code_viewer(target_dir, active_file)
