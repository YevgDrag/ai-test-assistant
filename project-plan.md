# Project Plan

## Objective

Build an AI-powered QA assistant that generates risk-aware test plans from Jira and Confluence artifacts and optionally creates draft test tasks.

## Milestones

### Milestone 1: Discovery and design
- Define user story and success criteria.
- Document Jira and Confluence data model requirements.
- Finalize the assistant architecture and prompt approach.

### Milestone 2: MVP backend and AI integration
- Build ingestion connectors for Jira and Confluence.
- Implement prompt templates and generation workflow.
- Return structured test plan drafts for review.

### Milestone 3: Validation and quality feedback
- Add coverage and consistency checks.
- Implement plan scoring and gap detection.
- Surface reviewer guidance and refinement prompts.

### Milestone 4: Jira / Confluence export
- Support draft issue creation in Jira.
- Support draft page creation in Confluence.
- Add traceability links to source requirements.

### Milestone 5: User workflow and handoff
- Build a simple UI or CLI for end-to-end flow.
- Add review, approve, and export steps.
- Document usage and setup.

## Timeline

- Week 1: baseline, architecture, and prototype stack.
- Week 2: connector build and first prompt-driven test plan generation.
- Week 3: validation layer and quality metrics.
- Week 4: Jira/Confluence export and workflow polish.

## Risks and mitigations

- Risk: source content is inconsistent or incomplete.
  - Mitigation: require explicit acceptance criteria extraction and missing-data warnings.
- Risk: Atlassian permissions add complexity.
  - Mitigation: keep write operations optional and support a manual export mode.
- Risk: generated test plans are too generic.
  - Mitigation: enforce structured prompts and risk-category mapping.
