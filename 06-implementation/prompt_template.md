# Prompt Template for AI QA Assistant Prototype

Use this template as the basis for generating the test plan from Jira and Confluence content.

## Prompt structure

1. Jira issue summary
2. Jira issue description
3. Acceptance criteria list
4. Confluence excerpt / additional context
5. Whether frontend changes are included
6. Whether design is available

## Example prompt

```
You are a QA assistant.

Jira Key: {{jira_key}}
Summary: {{jira_summary}}
Description: {{jira_description}}
Acceptance criteria:
- {{acceptance_criteria[0]}}
- {{acceptance_criteria[1]}}
- ...

Confluence notes:
{{confluence_excerpt}}

Is this a frontend change? {{frontend_changes}}
Is design available? {{design_available}}
Additional context:
{{additional_context}}

Task:
1. Provide a list of suggested checks that should be run for this issue.
2. For each suggested check, explain why it is important and how to verify it.
3. If this is a frontend change, ask whether design assets are available.
4. Provide a final test plan outline as numbered bullet points.
```

## Use case

- This template is used by the prototype service to structure the QA assistant's response.
- It is designed for initial MVP behavior without write-back to Jira.
