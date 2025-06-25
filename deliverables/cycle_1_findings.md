# DW7 Workflow - Cycle 1 Findings

This document tracks all flaws, bugs, and improvement points discovered during the initial observational cycle of the DW7 protocol.

## 1. Workflow Automation Gaps (`start-project-dw7.md`)

*   **Finding:** The workflow script references a `dw6 setup` command that is not implemented in the `dw6` CLI tool.
*   **Impact:** This breaks the automated setup process, requiring manual intervention for Git initialization, remote configuration, and the initial push.
*   **Suggestion:** Implement the `dw6 setup` command or update the workflow documentation to reflect the manual steps required.

## 2. Missing `.gitignore` in Template

*   **Finding:** The base project template does not include a `.gitignore` file.
*   **Impact:** The local virtual environment (`.venv`) and other transient files are incorrectly added to the Git repository during the initial commit.
*   **Suggestion:** Add a comprehensive Python `.gitignore` file to the root of the DW6 project template.

## 3. Unhandled Git Authentication

*   **Finding:** The workflow does not handle modern GitHub authentication requirements (Personal Access Tokens).
*   **Impact:** The `git push` command fails with a fatal authentication error when using standard HTTPS URLs.
*   **Suggestion:** The setup process (ideally an automated `setup` command) should configure the Git remote to use a PAT, or the documentation should explicitly guide the user through this configuration.

## 4. Brittle Integration Test

*   **Finding:** The integration test `test_approve_coder_stage_creates_deliverable` fails because it executes in a temporary directory that is not a Git repository.
*   **Impact:** The test suite is not self-contained and cannot run successfully without a pre-existing Git environment, reducing its reliability.
*   **Suggestion:** The test should be updated to create and use a temporary, mock Git repository to ensure it can run in isolation.
