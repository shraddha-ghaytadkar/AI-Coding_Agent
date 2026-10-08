# Autonomous AI Coding Agent

An autonomous, multi-file AI Coding Agent built with **Python**, **Groq / xAI API**, and **Streamlit**. Designed with **Clean Architecture** and strict adherence to **SOLID design principles**, this application provides a complete, demonstrable, end-to-end coding workflow.

---

## Features & Workflow

The agent follows an autonomous 7-step engineering pipeline:

```
[ User Coding Request ]
          │
          ▼
1. Task Understanding       -> Deconstructs natural language requirements & scope
          │
          ▼
2. Codebase AST Inspection  -> Scans multi-file repository & parses AST symbols
          │
          ▼
3. Relevance Identification  -> Identifies affected files with technical justification
          │
          ▼
4. Implementation Planning  -> Produces a structured Markdown architectural blueprint
          │
          ▼
5. Code Modification       -> Synthesizes validated, complete source code changes
          │
          ▼
6. Diff Synthesis           -> Computes unified diffs highlighting precise modifications
          │
          ▼
7. Sandbox Test Validation   -> Executes automated unit tests in an isolated sandbox
          │
          ▼
[ Final Result Presentation ]  -> Displays diffs, explanations, and test metrics
```

---

## Architectural Design & SOLID Principles

The system is separated into decoupled layers to guarantee maintainability, extensibility, and testability:

```
AIApp/
├── core/                   # Domain entities, DTOs, and abstract protocols (ISP, DIP)
│   ├── config.py           # Configuration management & environment variable bindings
│   ├── exceptions.py       # Domain exception hierarchy (AgentBaseException)
│   ├── interfaces.py       # Abstract interfaces (ILLMProvider, IInspector, IPlanner, etc.)
│   └── models.py           # Domain models (WorkflowState, ImplementationPlan, CodePatchResult)
├── services/               # Concrete service implementations (SRP, OCP, LSP)
│   ├── llm/
│   │   ├── base.py         # BaseLLMProvider (ABC)
│   │   ├── grok.py         # GrokLLMProvider (API communication with retry logic)
│   │   └── mock.py         # MockLLMProvider (offline evaluation & testing)
│   ├── inspector.py        # CodebaseInspector (filesystem crawler & AST parser)
│   ├── relevance.py        # RelevanceAnalyzer (identifies target files via LLM)
│   ├── planner.py          # ImplementationPlanner (generates architectural plans)
│   ├── coder.py            # CodeModificationEngine (generates code changes & unified diffs)
│   ├── validator.py        # SubprocessValidator (runs test suites in isolated sandbox)
│   └── repo_loader.py      # GitHubRepoLoader (clones remote repositories)
├── orchestrator/           # Workflow orchestration & Dependency Injection
│   ├── factory.py          # Dependency Injection Container (create_orchestrator)
│   └── workflow.py         # State machine coordinator (AgentWorkflowOrchestrator)
├── sample_codebases/       # Included multi-file Python repositories with test suites
│   ├── task_tracker/       # Task manager (models.py, service.py, utils.py, test_service.py)
│   ├── shopping_cart/      # E-commerce cart (cart.py, discounts.py, tax_calculator.py, test_cart.py)
│   └── user_auth/          # Auth system (user_db.py, password_hasher.py, authenticator.py, test_authenticator.py)
├── tests/                  # Automated unit and integration test suite
│   ├── test_inspector.py
│   ├── test_validator.py
│   └── test_orchestrator.py
├── frontend/               # Presentation Layer (Modular UI components & styling)
│   ├── components/         # Reusable widgets (header, sidebar, workflow_view, code_viewer)
│   ├── dashboard.py        # Dashboard controller unifying all UI components
│   └── styles.py           # CSS design system, typography, and styling tokens
├── app.py                  # Lightweight application entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Environment configuration template
└── .gitignore              # Protects secrets, bytecode, and temporary sandbox directories
```

### SOLID Principles Adherence Matrix

| Principle | Application in this Codebase |
| :--- | :--- |
| **Single Responsibility (SRP)** | Each component has a single reason to change: `SubprocessValidator` handles test execution; `RelevanceAnalyzer` evaluates file relevance; `CodebaseInspector` parses syntax trees. |
| **Open/Closed (OCP)** | New LLM providers (e.g. Anthropic, OpenAI, local Ollama) or validators (e.g. Pytest, Flake8) can be added by implementing interfaces without modifying workflow logic. |
| **Liskov Substitution (LSP)** | `MockLLMProvider` and `GrokLLMProvider` can be used interchangeably anywhere `BaseLLMProvider` is required. |
| **Interface Segregation (ISP)** | Client modules depend on specific, focused interfaces (`IRelevanceAnalyzer`, `IPlanGenerator`, `ICodePatcher`, `ICodeValidator`) rather than monolithic interfaces. |
| **Dependency Inversion (DIP)** | High-level orchestrators depend strictly on abstractions (`core.interfaces.*`). Dependencies are injected via `orchestrator.factory.create_orchestrator`. |

---

## Built-in Sample Codebases

The project includes three multi-file sample repositories equipped with test suites:

1. **Task Tracker Service** (`sample_codebases/task_tracker/`)
   - `models.py`: Task dataclass with priority and completion lifecycle.
   - `service.py`: TaskManager domain operations.
   - `utils.py`: Input validation, UUID generation, priority filters.
   - `test_service.py`: Unit test suite.

2. **Shopping Cart Calculator** (`sample_codebases/shopping_cart/`)
   - `cart.py`: ShoppingCart domain model with item aggregation and subtotal logic.
   - `discounts.py`: Coupon verification and percentage discount rules.
   - `tax_calculator.py`: Regional sales tax engine.
   - `test_cart.py`: Unit test suite.

3. **User Authentication System** (`sample_codebases/user_auth/`)
   - `user_db.py`: In-memory user store and account state tracking.
   - `password_hasher.py`: Salted SHA-256 cryptographic hashing.
   - `authenticator.py`: Auth controller with brute-force lockout safeguards.
   - `test_authenticator.py`: Unit test suite.

Additionally, the application supports cloning any public GitHub repository directly into the workspace for inspection and modification.

---

## Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git

### 2. Clone Repository
```bash
git clone https://github.com/123shraddha555/AI-Coding_Agent.git
cd AI-Coding_Agent
```

### 3. Create Virtual Environment
```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and set your API key:
```ini
GROK_API_KEY=your_actual_api_key
DEFAULT_TIMEOUT_SECONDS=30
```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## Running the Test Suite

The repository includes unit and end-to-end integration tests:
```bash
python -m unittest discover tests
```

---

## Deployment Guide

### Deploy to Streamlit Community Cloud
1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New App**, select repository `123shraddha555/AI-Coding_Agent`, branch `main`, and main file path `app.py`.
4. In **Advanced Settings**, add the secret:
   ```toml
   GROK_API_KEY = "your_actual_api_key"
   ```
5. Click **Deploy**.

### Deploy to Render
1. Create a **New Web Service** connected to your repository.
2. Set Environment to **Python 3**.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Add Environment Variable `GROK_API_KEY`.

---

## Security & Safety Controls

1. **Zero Secret Leakage**: API keys and environment configurations are excluded via `.gitignore`. Keys are never echoed in logs or committed.
2. **Ephemeral Sandbox Isolation**: The validator executes tests in temporary directories (`tempfile.mkdtemp`), preventing unintended modifications to the host working directory.
3. **Execution Timeouts**: Subprocess execution is guarded by strict timeouts (default 30s) to prevent infinite loops or hanging processes.
4. **AST Syntax Verification**: Modified code is checked with Python's built-in `ast.parse` prior to validation execution.

---

## Assumptions & Limitations

- **Assumptions**:
  - Python is present in the host environment to execute unit test validation suites.
  - Target codebases are self-contained or standard-library driven.
- **Limitations**:
  - Dynamic execution is currently specialized for Python test suites (`unittest`/`pytest`).
  - Network-dependent integrations within sample test suites are restricted in isolated sandboxes.
