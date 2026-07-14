# Architecture Overview

## Goal

Design a modular assistant for generating QA test plans, integrating product knowledge, and automating Jira/Confluence interactions.

## Components

1. Ingestion
   - Jira connector: fetch issue summary, description, acceptance criteria, epic/link fields, and comments.
   - Confluence connector: ingest page content, section headings, tables, and attachments.
   - Optional GitHub/GitLab issue importers in later phases.

2. Analysis Engine
   - Requirement extractor: turns source text into product capabilities, user goals, constraints, and acceptance criteria.
   - Risk taxonomy module: maps requirements to risk categories (functional, integration, regression, security, usability, performance).
   - Test scope planner: selects test objectives and coverage areas.
   - Traceability mapper: aligns test cases to source issues and acceptance criteria.

3. Test Plan Generator
   - Structured plan template engine for objectives, assumptions, test scenarios, test data, execution steps, and exit criteria.
   - Jira/Confluence artifact generator for page drafts or task descriptions.
   - Prioritisation logic for high-risk/significant coverage first.

4. Integration & Orchestration
   - API layer for Jira/Confluence operations and credentials management.
   - Workflow engine for `analyze -> generate -> review -> export` steps.

5. Validation & Feedback
   - Consistency checks for missing acceptance criteria or uncovered requirements.
   - Quality scoring and reviewer guidance annotations.
   - Iteration support for refining plans based on feedback.

## Data flow

1. User selects a Jira issue or Confluence page.
2. Ingestion connectors retrieve relevant content.
3. Analysis Engine extracts requirements and maps risk coverage.
4. Test Plan Generator builds a draft plan and relates it back to the source.
5. Validation module scores completeness and flags gaps.
6. Exporter writes a Jira issue draft or Confluence page draft, if permitted.
