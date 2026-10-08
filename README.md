# Autonomous AI Coding Agent

An enterprise-ready, multi-file autonomous software engineering assistant that analyzes natural language requirements, inspects multi-file codebases via Abstract Syntax Tree (AST) parsing, generates structured architectural plans, synthesizes precise code modifications with unified diffs, and validates changes within isolated execution sandboxes.

---

## Executive Summary

Modern software development workflows require continuous maintenance, bug fixing, and feature additions across complex, multi-file codebases. The **Autonomous AI Coding Agent** bridges the gap between natural language developer intent and validated production code.

Operating across a modular 7-stage autonomous pipeline, the agent:
1. Translates high-level feature requests and bug reports into technical objectives.
2. Explores codebase file trees and extracts AST symbols (classes, functions, methods, imports).
3. Evaluates project dependencies to pinpoint exactly which files require updates.
4. Produces an architectural implementation blueprint before applying modifications.
5. Generates syntactically validated code replacements.
6. Computes standard unified diffs for transparent code review.
7. Executes unit tests inside an isolated, non-destructive sandbox environment and reports metrics.

---

## Key Capabilities

- **Multi-File Context Understanding**: Parses multi-tier projects using Python's native Abstract Syntax Tree (`ast`) parser to understand code structure without consuming token budget on boilerplate.
- **Targeted Relevance Filtering**: Employs heuristic and LLM-driven dependency analysis to isolate relevant files, avoiding unnecessary changes to unrelated modules.
- **Architectural Planning**: Synthesizes structured implementation blueprints specifying design rationales, edge cases, and file-by-file action plans.
- **Unified Diff Synthesis**: Uses standard line-by-line diff formatting (`difflib`) to present changes clearly for human review.
- **Ephemeral Sandbox Validation**: Spins up temporary isolated environments (`tempfile.mkdtemp`) to run test suites safely via subprocesses with strict timeout safeguards, preventing host workspace corruption.
- **Interactive Code Viewer & Explorer**: Built-in VS Code-style sidebar explorer and top-level code viewer tab allowing real-time browsing of project files and AST symbols.
- **Remote GitHub Repository Cloner**: Supports testing arbitrary public GitHub repositories through dynamic shallow cloning (`git clone --depth 1`).
- **Resilient Multi-Endpoint Inference**: Built-in auto-detection and exponential backoff retry logic supporting both Groq Cloud LPU acceleration and xAI Grok APIs.

---

## Pipeline Workflow

```
[Developer Prompt] + [Target Codebase / Git Repo]
                      |
                      v
          [1. Codebase Inspector]
          (Recursive Crawl + AST Symbol Extraction)
                      |
                      v
          [2. Relevance Analyzer]
          (Dependency Mapping & Affected File Selection)
                      |
                      v
          [3. Implementation Planner]
          (Step-by-Step Architectural Plan)
                      |
                      v
          [4. Code Patcher & Diff Engine]
          (Code Synthesis & Unified Diff Generation)
                      |
                      v
          [5. Isolated Sandbox Validator]
          (Temporary Workspace + Subprocess Test Execution)
                      |
                      v
       [Streamlit Interactive Dashboard]
       (Review Diffs, Execution Metrics, Test Logs)
```

---

## Technical Stack

| Layer | Technologies & Libraries |
| :--- | :--- |
| **Runtime Environment** | Python 3.10+ (tested on Python 3.12) |
| **Inference Engines** | Groq Cloud LPU (`openai/gpt-oss-120b`, `qwen/qwen3.8-27b`)<br>xAI API (`grok-2-latest`) |
| **Web Presentation** | Streamlit, Responsive CSS Custom Design System |
| **Code Parsing & AST** | Python Standard Library `ast` (Classes, Functions, Methods, Imports) |
| **Diff Synthesis** | Python Standard Library `difflib` (Unified Diff format) |
| **Sandboxing & Execution** | Python `subprocess`, `tempfile.mkdtemp`, `unittest` framework |
| **Version Control Integration** | Git CLI (shallow cloning `--depth 1`) |
| **Configuration & Secrets** | `python-dotenv`, Environment Variable Isolation |
| **HTTP & Networking** | `urllib.request` / `http.client` (Zero external HTTP dependency overhead) |

---

## Project Structure

```
AIApp/
├── core/                               # Core configuration and domain interfaces
│   ├── config.py                       # Runtime settings, timeout guards, and LLM key detection
│   ├── exceptions.py                   # Domain-specific exception hierarchy
│   ├── interfaces.py                   # Protocol definitions for all service contracts
│   └── models.py                       # Dataclasses (CodebaseContext, PatchResult, TestRunResult)
├── services/                           # Modular business logic services
│   ├── llm/
│   │   ├── base.py                     # Abstract base class for LLM providers
│   │   ├── grok.py                     # Groq Cloud & xAI provider with exponential backoff
│   │   └── mock.py                     # Offline mock provider for testing
│   ├── inspector.py                    # Filesystem crawler and AST symbol extractor
│   ├── relevance.py                    # Context analyzer targeting affected project files
│   ├── planner.py                      # Architectural step-by-step plan generator
│   ├── coder.py                        # Code modification engine and unified diff synthesizer
│   ├── validator.py                    # Ephemeral sandbox runner with subprocess isolation
│   └── repo_loader.py                  # Remote GitHub repository cloner
├── orchestrator/                       # Pipeline state coordinator
│   ├── factory.py                      # Dependency injection and service assembly
│   └── workflow.py                     # Autonomous 7-stage state machine orchestrator
├── sample_codebases/                   # Built-in multi-file test projects
│   ├── task_tracker/                   # Task management application with unit tests
│   │   ├── models.py                   # Task data models and status enums
│   │   ├── service.py                  # Task lifecycle management operations
│   │   ├── utils.py                    # Validation, UUID generation, filtering helpers
│   │   └── test_service.py             # Unit test suite
│   ├── shopping_cart/                  # E-commerce cart system with discounts and tax
│   │   ├── cart.py                     # Cart item aggregation and coupon logic
│   │   ├── discounts.py                # Discount rules and percentage algorithms
│   │   ├── tax_calculator.py           # Regional tax rate computations
│   │   └── test_cart.py                # Unit test suite
│   └── user_auth/                      # Authentication service with security features
│       ├── user_db.py                  # In-memory user credentials store
│       ├── password_hasher.py          # Salted SHA-256 cryptographic hashing
│       ├── authenticator.py            # Login validation and lockout protection
│       └── test_authenticator.py       # Unit test suite
├── frontend/                           # Streamlit user interface components
│   ├── components/
│   │   ├── header.py                   # Top branding bar and status indicators
│   │   ├── sidebar.py                  # Codebase selector, GitHub cloner, and file tree
│   │   ├── workflow_view.py            # Pipeline phases, diffs, and execution logs
│   │   └── code_viewer.py              # VS Code-style file previewer with AST inspection
│   ├── dashboard.py                    # Primary navigation controller (Tabs: Workflow / Code Viewer)
│   └── styles.py                       # Modern typography, glassmorphism, and color system
├── tests/                              # Automated test suite
│   ├── test_inspector.py               # Unit tests for AST scanning and symbol extraction
│   ├── test_validator.py               # Unit tests for sandbox test execution
│   └── test_orchestrator.py            # Integration tests for end-to-end agent workflow
├── app.py                              # Application entry point
├── requirements.txt                    # Python package dependencies
├── .env.example                        # Template for environment configuration
└── .gitignore                          # Git exclusions (credentials, caches, virtual environments)
```

---

## Included Sample Codebases

The application includes three pre-packaged multi-file Python projects designed to demonstrate the agent's capabilities across distinct architectural patterns:

### 1. Task Tracker Service (`sample_codebases/task_tracker/`)
A domain-driven task management application supporting creation, status transitions, priority filtering, and tag management.
- **Files**: `models.py`, `service.py`, `utils.py`, `test_service.py`
- **Example Prompts**:
  - *"Add a dueDate field to Task with validation and add overdue task filtering to TaskService."*
  - *"Add priority-based sorting to TaskService.get_tasks."*

### 2. Shopping Cart Calculator (`sample_codebases/shopping_cart/`)
A financial calculation engine handling multi-item subtotaling, tiered coupon discounts, and regional sales tax.
- **Files**: `cart.py`, `discounts.py`, `tax_calculator.py`, `test_cart.py`
- **Example Prompts**:
  - *"Add support for a BUY2GET1 coupon that discounts the lowest priced item."*
  - *"Add bulk quantity discount: 5% off items with quantity of 5 or more."*

### 3. User Authentication System (`sample_codebases/user_auth/`)
A security module handling salted password hashing, user registration, authentication, and brute-force account lockout protection.
- **Files**: `user_db.py`, `password_hasher.py`, `authenticator.py`, `test_authenticator.py`
- **Example Prompts**:
  - *"Implement password expiration policy: reject logins if password is older than 90 days."*
  - *"Add an account unlock method with admin verification."*

---

## Getting Started

### 1. System Prerequisites
- **Python**: Version 3.10 or higher
- **Git**: Installed and available in your system `PATH`
- **Internet Access**: Required for LLM API calls and GitHub repository cloning

### 2. Clone the Repository
```bash
git clone https://github.com/123shraddha555/AI-Coding_Agent.git
cd AI-Coding_Agent
```

### 3. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the provided environment template:
```bash
cp .env.example .env
```
*(On Windows Command Prompt: `copy .env.example .env`)*

Edit `.env` to supply your API credentials:
```ini
# LLM API Key (Supports Groq Cloud 'gsk_...' or xAI 'xai-...')
GROK_API_KEY=gsk_your_groq_api_key_here

# Execution Safeguards
DEFAULT_TIMEOUT_SECONDS=30
MAX_RETRIES=3
```

> **API Key Compatibility**:
> - Keys starting with `gsk_` automatically route to **Groq Cloud** using ultra-fast LPUs (`openai/gpt-oss-120b`).
> - Keys starting with `xai-` automatically route to the **xAI API** (`grok-2-latest`).
> - API keys are managed exclusively in `.env` and are never exposed in the browser interface.

---

## Running the Application

### Launch Local Server
Execute the following command in your terminal:
```bash
streamlit run app.py
```

Once running, navigate to the local dashboard in your browser:
```
http://localhost:8501
```

### User Navigation Guide

1. **Target Codebase Selection**:
   - In the left sidebar, choose a built-in project (`Shopping Cart`, `Task Tracker`, or `User Auth`).
   - To inspect a custom project, use the **Clone GitHub Repository** section in the sidebar, paste any public GitHub repository URL, and click **Clone & Load**.
2. **Codebase Exploration**:
   - Click on any file listed under **Codebase Files** in the sidebar.
   - Switch to the **Code Viewer** tab on top to view the full source code alongside extracted AST symbols (classes, methods, functions).
3. **Task Execution**:
   - Switch to the **Agent Workflow** tab.
   - Enter your requirements into the task prompt box or select one of the suggested sample prompts.
   - Click **Run Agent Pipeline**.
4. **Inspecting Results**:
   - **Phase 1 (Inspection & Relevance)**: View scanned files and the justification for selecting specific targets.
   - **Phase 2 (Implementation Plan)**: Read the step-by-step engineering plan.
   - **Phase 3 (Code Modifications & Diff Viewer)**: Inspect unified diffs showing additions and deletions.
   - **Phase 4 (Sandbox Validation)**: Review unit test execution results, pass/fail status, runtime duration, and captured standard output logs.

---

## Running the Test Suite

The project includes unit and integration tests verifying the AST inspector, sandbox execution runner, and end-to-end pipeline orchestrator.

### Run All Tests
```bash
python -m unittest discover tests
```

### Run Specific Test Modules
```bash
# Test AST inspection and symbol extraction
python -m unittest tests/test_inspector.py

# Test sandbox creation and test execution
python -m unittest tests/test_validator.py

# Test orchestrator pipeline state machine
python -m unittest tests/test_orchestrator.py
```

Expected output:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.28s

OK
```

---

## Cloud Deployment Guide

### Deploying to Streamlit Community Cloud
1. Push your repository to your GitHub account (`123shraddha555/AI-Coding_Agent`).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New App** and configure:
   - **Repository**: `123shraddha555/AI-Coding_Agent`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Expand **Advanced Settings** and add your secret in the **Secrets** section:
   ```toml
   GROK_API_KEY = "gsk_your_actual_key_here"
   ```
5. Click **Deploy**.

### Deploying to Render
1. Log in to [Render](https://render.com/) and select **New Web Service**.
2. Connect your GitHub repository `123shraddha555/AI-Coding_Agent`.
3. Configure the service settings:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
4. Add the environment variable:
   - Key: `GROK_API_KEY`
   - Value: `gsk_your_actual_key_here`
5. Click **Create Web Service**.

---

## Security & Reliability Architecture

- **Zero Host Mutation**: Test execution runs entirely inside ephemeral directories created with `tempfile.mkdtemp`. Source code in the repository remains untouched unless explicitly exported.
- **Subprocess Isolation**: Test suites are executed in sandboxed subprocesses with rigid timeouts (default 30 seconds), preventing malicious or runaway test loops from exhausting host memory or CPU.
- **Syntax Pre-Flight Verification**: Modified code is validated via Python's AST compiler (`ast.parse`) before reaching the sandbox, catching syntax errors immediately.
- **Credential Protection**: API keys are loaded via backend environment variables and excluded from git history via `.gitignore`. No credentials are sent to the client or rendered in the DOM.
- **Exponential Backoff**: Inference calls incorporate automated retry logic with exponential backoff to handle rate limits and transient network interruptions gracefully.

---

## License

This project is licensed under the MIT License. See [LICENSE](file:///c:/Users/hp/Downloads/AIApp/LICENSE) for details.
