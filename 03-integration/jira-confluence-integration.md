# Jira / Confluence Integration

## Objectives

- Read Jira issue data and Confluence requirement pages.
- Generate test plans that can be attached to Jira tickets.
- Optionally create draft test tasks in Jira and draft documentation in Confluence.

## Jira Integration

- Use Jira REST API or Atlassian Forge connectors.
- Required permissions:
  - `read:issue` and `read:comment`
  - `write:issue` for creating test tasks or linking artifacts
- Map fields:
  - `summary`, `description`, `acceptance criteria`, `priority`, `labels`, `components`
  - `linked issues` and `epic` for traceability
- Create test task templates with:
  - `Test objective`
  - `Test scenarios`
  - `Preconditions`
  - `Steps`
  - `Expected results`
  - `Test data`
  - `Risks`

## Confluence Integration

- Use Confluence REST API for page retrieval and page creation.
- Required access:
  - `read:content`
  - `write:content` for publishing plan drafts
- Extract structured content from:
  - headings, tables, definition lists, and attachments
- Export generated test plan as:
  - a Confluence page draft, or
  - a section added to an existing product requirements page

## Authentication

- Support API token + email basic auth for Atlassian Cloud.
- Support OAuth 2.0 / app links for enterprise Atlassian.
- Store credentials securely in environment or a secrets manager.

## Integration considerations

- Respect user permissions and audit trails.
- Keep writes optional until draft review is complete.
- Support a manual export mode for users who want no changes to Jira/Confluence.
