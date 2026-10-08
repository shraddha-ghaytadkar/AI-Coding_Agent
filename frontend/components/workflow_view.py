"""
Workflow progress and result visualization component.
Renders step cards, diffs, test metrics, and telemetry logs.
Clean presentation without emojis.
"""
import os
import streamlit as st
from core.models import WorkflowStep, WorkflowState


def render_workflow_results(state: WorkflowState):
    """Renders all workflow artifact cards given an executed WorkflowState."""
    if not state:
        return

    st.markdown("---")

    # Header Status Bar
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        if state.current_step == WorkflowStep.COMPLETED:
            st.markdown('<span class="badge-success">Status: Succeeded</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-danger">Status: Failed</span>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"**Target Codebase:** `{os.path.basename(state.codebase_path)}`")
    with col_s3:
        if state.validation_result:
            val_badge = (
                '<span class="badge-success">Validation Passed</span>'
                if state.validation_result.passed
                else '<span class="badge-danger">Validation Failed</span>'
            )
            st.markdown(f"**Test Suite:** {val_badge}", unsafe_allow_html=True)

    if state.current_step == WorkflowStep.FAILED and state.error_message:
        st.error(f"Workflow Execution Error: {state.error_message}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Step 1 & 2: Understanding & Relevance
    with st.container():
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Phase 1: Task Understanding & Codebase Relevance</div>
            """,
            unsafe_allow_html=True,
        )
        if state.relevance_result:
            st.markdown("**Identified Files:**")
            badges_html = "".join(
                [f'<span class="badge-tag">{f}</span>' for f in state.relevance_result.selected_files]
            )
            st.markdown(badges_html, unsafe_allow_html=True)
            st.markdown(f"**Reasoning:** {state.relevance_result.reasoning}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Step 3: Implementation Plan
    with st.container():
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Phase 2: Architectural Implementation Plan</div>
            """,
            unsafe_allow_html=True,
        )
        if state.plan:
            st.markdown(state.plan.markdown_plan)
        st.markdown("</div>", unsafe_allow_html=True)

    # Step 4 & 5: Proposed Changes & Unified Diff
    with st.container():
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Phase 3: Code Modifications & Unified Diff</div>
            """,
            unsafe_allow_html=True,
        )
        if state.patch_result:
            st.markdown(f"**Summary of Changes:** {state.patch_result.explanation}")

            diff_tabs = st.tabs(list(state.patch_result.modified_files.keys()))
            for i, (fname, new_content) in enumerate(state.patch_result.modified_files.items()):
                with diff_tabs[i]:
                    diff_text = state.patch_result.diffs.get(fname, "")
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.markdown(f"**Unified Diff (`{fname}`)**")
                        st.code(diff_text, language="diff")
                    with col_d2:
                        st.markdown(f"**Updated Source (`{fname}`)**")
                        st.code(new_content, language="python")

        st.markdown("</div>", unsafe_allow_html=True)

    # Step 6: Sandbox Validation
    with st.container():
        st.markdown(
            """
            <div class="step-card">
                <div class="step-title">Phase 4: Automated Sandbox Validation</div>
            """,
            unsafe_allow_html=True,
        )
        if state.validation_result:
            res = state.validation_result
            col_v1, col_v2, col_v3 = st.columns(3)
            with col_v1:
                st.metric("Total Tests Executed", res.total_tests)
            with col_v2:
                st.metric("Passed Tests", res.passed_tests)
            with col_v3:
                st.metric("Execution Duration", f"{res.duration_seconds}s")

            st.markdown("**Test Runner Console Output:**")
            st.code(res.output_log, language="bash")

        st.markdown("</div>", unsafe_allow_html=True)

    # Telemetry Logs
    with st.expander("Execution Telemetry Logs"):
        for log in state.logs:
            st.text(log)
