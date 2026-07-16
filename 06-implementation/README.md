# AI QA Assistant Prototype

This folder contains a prototype Python API for the AI QA assistant.

## Install dependencies

From the project root:

```cmd
cd C:\Projects\ai-test-assistant\06-implementation
python -m pip install -r requirements.txt
```

## Run the prototype server

```cmd
uvicorn app:app --reload --port 8000
```

## Example request

Create a file `payload.json` with:

```json
{
  "jira_key": "PROJ-101",
  "jira_summary": "Implement payment method X",
  "jira_description": "Users must be able to add and use payment method X in checkout.",
  "acceptance_criteria": [
    "Users can add payment method X",
    "Payment method X appears in checkout",
    "Error is shown for invalid data"
  ],
  "confluence_excerpt": "The payment flow should support saved cards and use secure handling.",
  "confluence_file_path": "confluence.txt",
  "frontend_changes": true,
  "design_available": false,
  "additional_context": "Release target 2026-08-01."
}
```

Send the request:

```cmd
curl -X POST http://127.0.0.1:8000/generate-test-plan ^
  -H "Content-Type: application/json" ^
  -d @payload.json
```

If you want to load Confluence requirements from a separate local file instead of the JSON field,
set `confluence_file_path` in payload.json and create that file next to `app.py`.

Example `confluence.txt` content:

```
The payment flow should support saved cards and use secure handling.
Users can remove saved cards from checkout.
Payment method X is available only for logged-in users.
```

Then send the same request again. The service will read the file and include it in the analysis.

Expected output:

- `plan_markdown` with a structured test plan
- `suggested_checks` list
- `qa_confirm_question` text

If you want a more readable plain-text response with real line breaks, use:

```cmd
curl -X POST http://127.0.0.1:8000/generate-test-plan/plain ^
  -H "Content-Type: application/json" ^
  -d @payload.json
```

This second endpoint returns just the test plan text, so you can read it directly without escaped `\n` characters.

## Notes

- This prototype does not write back to Jira.
- Use `prompt_template.md` to shape the testing logic for a future LLM-based generation.
