# Prototype Implementation Stack

## Goals

- Deliver a working AI assistant that can generate high-quality test plans from Jira and Confluence inputs.
- Keep the first version lightweight, extensible, and easy to deploy.

## Recommended stack

### Core AI / LLM
- Use a managed LLM service with strong prompt engineering support, such as OpenAI, Anthropic, or Azure OpenAI.
- Start with a text generation model for structured plan creation and validation.
- Consider local or open-source alternatives later for additional control.

### Backend
- Language: Python or TypeScript/Node.js.
- Framework: FastAPI (Python) or Express / NestJS (Node.js).
- Orchestration: simple REST API with `analyze`, `generate`, and `export` endpoints.

### Data connectors
- Jira: Atlassian REST API via `jira` Python package or `@atlassian/jira` Node SDK.
- Confluence: Atlassian REST API for page read/create operations.
- Secrets: environment variables or a vault-like secrets store.

### Prompting and plan generation
- Use prompt templates with sections for:
  - source context,
  - acceptance criteria,
  - risk categories,
  - test objectives,
  - test scenarios,
  - execution steps.
- Store prompt templates as reusable JSON/YAML assets.

### Storage and caching
- Minimal MVP: no persistent database required.
- Keep request payloads and generated drafts in-memory or in temporary storage.
- Later: add lightweight database (SQLite / PostgreSQL) for audit trail and plan history.

### UI / UX
- MVP options:
  - command-line tool,
  - lightweight web UI,
  - Jira/Confluence app integration.
- Initial priority: validation and export workflow via REST and simple browser UI if time permits.

### Validation
- Implement a plan quality checker that examines generated output.
- Use a second prompt or deterministic rule set to verify:
  - coverage of acceptance criteria,
  - explicit risk mapping,
  - presence of expected results.

## Phased rollout

1. MVP: read Jira/Confluence, generate draft plan, return plain text or markdown.
2. Integration: write back Jira test tasks and Confluence draft pages.
3. Feedback: capture reviewer notes, refine prompts, add iterative revision support.
