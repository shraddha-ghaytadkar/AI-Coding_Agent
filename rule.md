# AI Coding Agent Assignment --- Rules for Antigravity

## 1. Assignment Objective

Build and deploy a small AI Coding Agent that can:

-   Understand a developer's coding request written in natural language.
-   Analyze a selected sample codebase/project.
-   Identify the files relevant to the requested task.
-   Propose or make code changes.
-   Clearly explain the changes.
-   Show the changed files or a patch/diff.
-   Validate the proposed changes using at least one meaningful
    validation step, test, or demo case.

The goal is a working end-to-end coding-agent flow, not a large
unfinished system.

------------------------------------------------------------------------

## 2. Codebase Rules

-   Use a small sample repository/project created specifically for the
    application, or another suitable sample repository.
-   The sample project must contain multiple files.
-   The agent must be able to read multiple files from the project.
-   The agent must identify which files are relevant to the user's
    coding request.
-   Do not assume that users must provide their own GitHub repository; a
    built-in sample project is sufficient.
-   Keep the sample codebase small enough that the complete workflow
    remains reliable and easy to demonstrate.

------------------------------------------------------------------------

## 3. User Interface Rules

Provide either a simple web UI or CLI.

The application must allow the user to:

1.  Enter a coding task in natural language.
2.  Start the agent workflow.
3.  See the agent's plan before or while changes are being made.
4.  Clearly see the relevant files selected by the agent.
5.  See the proposed changes or generated patch/diff.
6.  Understand what was changed and why.
7.  See the validation result.

Keep the interface simple and focused on the coding-agent workflow.

------------------------------------------------------------------------

## 4. Required Agent Workflow

The agent should follow this general flow:

``` text
User Coding Request
        ↓
Understand Task
        ↓
Inspect Sample Codebase
        ↓
Identify Relevant Files
        ↓
Generate Implementation Plan
        ↓
Propose / Make Code Changes
        ↓
Generate Diff / Changed Files
        ↓
Validate Changes
        ↓
Show Final Result
```

The implementation may use an LLM, agentic flow, tool-calling,
retrieval, or a combination where appropriate.

------------------------------------------------------------------------

## 5. Agent Behaviour

The agent must be able to:

-   Understand the intent of the coding request.
-   Inspect relevant source files.
-   Select files related to the requested change.
-   Produce a clear implementation plan.
-   Suggest or make appropriate code changes.
-   Explain what was changed and why.
-   Present the changed files or a diff/patch.
-   Perform a meaningful validation step, test, or demo case.
-   Clearly report whether validation succeeded or failed.

Do not build unnecessary features that do not contribute to this flow.

------------------------------------------------------------------------

## 6. Validation Rules

The application must include at least one meaningful:

-   Test,
-   Validation step, or
-   Demo case.

Validation should be performed after the proposed changes where
practical.

The application should clearly display the validation result.

------------------------------------------------------------------------

## 7. Deployment Rules

The application must be deployed and accessible online.

Suitable platforms include, but are not limited to:

-   Render
-   Vercel
-   Netlify
-   Railway
-   Hugging Face Spaces
-   Streamlit Cloud
-   Any equivalent suitable platform

The deployed application must be usable by a reviewer.

------------------------------------------------------------------------

## 8. README Requirements

The GitHub repository must include a clear README containing:

-   Project overview
-   Setup instructions
-   How to run the project locally
-   Project/agent approach
-   How the coding-agent workflow works
-   Assumptions
-   Limitations
-   Any required environment variables or configuration
-   Deployment information where useful

------------------------------------------------------------------------

## 9. Security Rules

-   Never commit API keys.
-   Never commit passwords.
-   Never commit secrets.
-   Use environment variables or the deployment platform's
    secret-management mechanism.
-   Do not expose credentials in the UI, source code, README, or Git
    history.

------------------------------------------------------------------------

## 10. Code Quality Rules

The implementation should have:

-   Clean project structure.
-   Readable code.
-   Sensible naming.
-   Sensible error handling.
-   Clear separation between major responsibilities.
-   No unnecessary complexity.
-   No unrelated features.

Prefer a small, reliable implementation over a large incomplete system.

------------------------------------------------------------------------

## 11. Scope Rules

Keep the scope small but complete.

Prioritize:

1.  Working natural-language task input.
2.  Codebase inspection.
3.  Relevant-file identification.
4.  Agent plan.
5.  Code change / proposal.
6.  Diff or changed-file presentation.
7.  Validation.
8.  Deployment.
9.  README/documentation.

Do not spend significant effort on features that are not necessary for
the end-to-end assignment.

A user-uploaded repository or arbitrary GitHub repository support is
optional and is not a minimum requirement of the assignment.

------------------------------------------------------------------------

## 12. Evaluation Alignment

The implementation should directly demonstrate the following evaluation
areas:

### Agent Design

Show a clear flow from:

``` text
Task Understanding → File Selection → Code Change
```

### Practical Implementation

The application must actually work rather than only demonstrate a
concept.

### Code Quality

Use a clean structure, readable implementation, and sensible error
handling.

### AI Usage

Use an LLM/agentic flow/tool-calling/retrieval meaningfully where
applicable.

### Deployment

Provide a usable deployed application link.

### Communication

Provide a clear README and concise explanation of the approach.

------------------------------------------------------------------------

## 13. Final Submission Checklist

Before considering the assignment complete, verify:

-   [ ] Natural-language coding task can be entered.
-   [ ] Sample project/codebase contains multiple files.
-   [ ] Agent reads/analyzes multiple files.
-   [ ] Agent identifies relevant files.
-   [ ] Agent produces an implementation plan.
-   [ ] Agent proposes or makes code changes.
-   [ ] Changed files or diff are displayed.
-   [ ] Changes are explained.
-   [ ] At least one meaningful validation/test/demo exists.
-   [ ] Validation result is displayed.
-   [ ] Application works end-to-end.
-   [ ] Application is deployed online.
-   [ ] GitHub repository is ready.
-   [ ] README is included.
-   [ ] Assumptions are documented.
-   [ ] Limitations are documented.
-   [ ] No API keys, passwords, or secrets are committed.

## 14. Core Principle

Build a **small, reliable, demonstrable AI Coding Agent**.

The most important experience for the reviewer should be:

> Enter a coding task → watch the agent understand it → see the relevant
> files → see the plan → see the proposed change/diff → see validation →
> understand the final result.
