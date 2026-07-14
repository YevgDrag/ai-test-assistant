# AI QA Assistant

This project is for an AI assistant that generates structured test plans from Jira issues and Confluence requirements.

## What this assistant can be based on

- Managed LLM services such as OpenAI, Azure OpenAI, or Anthropic for the first MVP.
- A prompt-driven pipeline that converts Jira/Confluence text into test objectives, risk mapping, and scenario drafts.
- Later versions can add open-source models or a hybrid local/cloud approach.

## How the assistant can look and work

- The assistant can be a lightweight web UI, a CLI tool, or a backend API.
- Users provide a Jira issue key and/or a Confluence page link as input.
- The assistant ingests source text, then generates a markdown test plan with:
  - objective
  - scope and assumptions
  - risk summary
  - test scenarios
  - preconditions, steps, expected results
  - exit criteria
- Prompt input is assembled from issue summary, description, acceptance criteria, and requirement notes.

## Early usage model

- The first version can be an API request:
  - send Jira/Confluence data payload to the assistant,
  - receive a generated test plan draft in response.
- This makes it easy to start with a backend-only MVP and add a UI later.
- Write-back to Jira/Confluence should stay optional until the draft is reviewed.

## Structure

- `01-baseline/` - product thesis, goals, and success criteria
- `02-architecture/` - proposed system architecture and components
- `03-integration/` - Jira, Confluence, and toolchain integration design
- `04-validation/` - metrics, evaluation, and test automation strategy
- `05-notes/` - working notes and research
- `06-implementation/` - prototype stack proposal and prompt templates

## Example API request

Send a JSON payload containing the Jira issue data and optional Confluence content to the assistant API. Below is a minimal example payload and a `curl` request you can use from the command line.

Example JSON payload:

```json
{
  "jira_key": "PROJ-123",
  "jira_summary": "Add payment method X",
  "jira_description": "Users should be able to add payment method X via settings page.",
  "acceptance_criteria": [
    "User can add payment method X",
    "Payment method X is stored securely",
    "UI shows confirmation"
  ],
  "confluence_excerpt": "Optional design details or data format",
  "additional_context": "Release: 2026-08-01; Critical for checkout flow"
}
```

Minimal `curl` example (POSTs JSON and returns a markdown test plan):

```bash
curl -X POST https://ai-qa-assistant.local/api/v1/generate-test-plan \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '@payload.json'
```

Expected response: a JSON object with `plan_markdown` and a `validation_summary` field. Write-back to Jira/Confluence should be performed only after human review.

If you want, I can add a tiny example server stub (Python FastAPI) to the `06-implementation/` folder so you can test the API locally.
