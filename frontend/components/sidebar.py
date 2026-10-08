"""
Sidebar navigation and configuration component.
Includes dynamic codebase selector (built-in + cloned repositories),
GitHub repository cloner, and clean sidebar file explorer.
No emojis or static AI model names.
"""
import os
import streamlit as st
from core.config import get_config
from services.repo_loader import GitHubRepoLoader


def render_sidebar(base_dir: str, built_in_codebases: dict) -> tuple[str, str, str]:
    """
    Renders sidebar controls and returns:
    (selected_codebase_name, target_dir, active_file)
    """
    config = get_config()
    cloner_storage_dir = os.path.join(base_dir, "cloned_repos")
    repo_loader = GitHubRepoLoader(cloner_storage_dir)

    # Dynamically scan cloned_repos directory for any existing repositories
    all_codebases = dict(built_in_codebases)
    if os.path.exists(cloner_storage_dir):
        for item in sorted(os.listdir(cloner_storage_dir)):
            repo_path = os.path.join(cloner_storage_dir, item)
            if os.path.isdir(repo_path) and not item.startswith("."):
                label = f"GitHub: {item}"
                all_codebases[label] = {
                    "dir": repo_path,
                    "desc": f"Cloned repository from GitHub ({item})",
                    "sample_prompts": [
                        f"Analyze the repository structure and add documentation/comments in {item}",
                        f"Refactor helper functions and add unit test coverage in {item}",
                    ],
                }

    with st.sidebar:
        # Clean Header
        st.markdown(
            """
            <div style="margin-bottom: 12px;">
                <div style="font-weight: 700; font-size: 1.15rem; color: #f1f5f9; letter-spacing: -0.02em;">Coding Agent Dashboard</div>
                <div style="font-size: 0.78rem; color: #94a3b8;">Multi-File Code Modification Pipeline</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Backend AI Engine Status Indicator
        if config.has_api_key:
            st.markdown(
                """
                <div style="background-color: #064e3b; border: 1px solid #059669; border-radius: 6px; padding: 6px 12px; margin-bottom: 14px; font-size: 0.8rem; color: #34d399; display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 0.7rem;">●</span> <strong>Model Connected</strong> <span style="color: #a7f3d0; font-size: 0.75rem;">(backend .env)</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="background-color: #7f1d1d; border: 1px solid #dc2626; border-radius: 6px; padding: 6px 12px; margin-bottom: 14px; font-size: 0.8rem; color: #fca5a5;">
                    <strong>API Key Not Configured</strong><br>
                    <span style="font-size: 0.72rem; color: #fecaca;">Please configure your API key in the backend .env file.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        # Codebase Selection & Cloned Repositories Listing
        st.markdown("### Target Codebase")

        selection_options = list(all_codebases.keys()) + ["Clone from GitHub Repository..."]

        # Handle persistent selection across reruns
        saved_selected = st.session_state.get("selected_codebase_key")
        default_index = 0
        if saved_selected and saved_selected in selection_options:
            default_index = selection_options.index(saved_selected)

        selected_option = st.selectbox(
            "Select Codebase:",
            options=selection_options,
            index=default_index,
            label_visibility="collapsed",
            key="codebase_selector_dropdown",
        )
        st.session_state.selected_codebase_key = selected_option

        target_dir = ""
        selected_codebase_name = selected_option

        # Clone GitHub Repository Form
        if selected_option == "Clone from GitHub Repository...":
            st.markdown("**Remote Repository URL:**")
            github_url = st.text_input(
                "GitHub URL:",
                placeholder="https://github.com/username/repository",
                label_visibility="collapsed",
            )

            col_cl1, col_cl2 = st.columns([1, 1])
            with col_cl1:
                clone_btn = st.button("Clone Repository", use_container_width=True)

            if clone_btn:
                if not github_url.strip():
                    st.warning("Please enter a valid GitHub repository URL.")
                else:
                    with st.spinner("Cloning repository into workspace..."):
                        success, cloned_path, msg = repo_loader.clone_repository(github_url)
                        if success:
                            st.success(f"Repository cloned: {msg}")
                            repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")
                            new_label = f"GitHub: {repo_name}"
                            st.session_state.selected_codebase_key = new_label
                            st.rerun()
                        else:
                            st.error(f"Clone error: {msg}")

            # Fallback to first available codebase if not yet cloned
            first_key = list(all_codebases.keys())[0]
            target_dir = all_codebases[first_key]["dir"]
            selected_codebase_name = first_key
        else:
            codebase_info = all_codebases[selected_option]
            target_dir = codebase_info["dir"]
            selected_codebase_name = selected_option
            st.caption(codebase_info["desc"])

        st.markdown("---")

        # Sidebar File Explorer
        st.markdown("### Files Explorer")

        active_file = None
        if os.path.exists(target_dir):
            file_list = []
            for root, _, files in os.walk(target_dir):
                for f in sorted(files):
                    if f.endswith(".py") and not f.startswith("."):
                        rel = os.path.relpath(os.path.join(root, f), target_dir).replace("\\", "/")
                        file_list.append(rel)

            if file_list:
                current_active = st.session_state.get("active_file", file_list[0])
                if current_active not in file_list:
                    current_active = file_list[0]

                st.markdown(
                    f"""
                    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #89b4fa; margin-bottom: 4px; font-weight: 600;">
                        Project: {os.path.basename(target_dir)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                selected_file = st.radio(
                    "Files in workspace:",
                    options=file_list,
                    index=file_list.index(current_active) if current_active in file_list else 0,
                    label_visibility="collapsed",
                    key="sidebar_file_explorer",
                )

                st.session_state.active_file = selected_file
                active_file = selected_file
            else:
                st.info("No Python source files found in this workspace.")

        st.markdown("---")

        # Sample Prompts
        prompts = all_codebases.get(selected_option, {}).get("sample_prompts", [])
        if prompts:
            st.markdown("### Suggested Tasks")
            for prompt_example in prompts:
                if st.button(f"{prompt_example[:38]}...", key=f"prompt_{prompt_example}"):
                    st.session_state.current_prompt = prompt_example

    return selected_codebase_name, target_dir, active_file
