from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="AI QA Assistant Prototype")

class TestPlanRequest(BaseModel):
    jira_key: str
    jira_summary: str
    jira_description: str
    acceptance_criteria: List[str]
    confluence_excerpt: Optional[str] = None
    confluence_file_path: Optional[str] = None
    frontend_changes: Optional[bool] = False
    design_available: Optional[bool] = False
    additional_context: Optional[str] = None

class TestPlanResponse(BaseModel):
    plan_markdown: str
    suggested_checks: List[str]
    qa_confirm_question: str


def build_test_plan(request: TestPlanRequest) -> TestPlanResponse:
    def normalize_check(text: str) -> str:
        text = text.strip().rstrip('.')
        if not text:
            return ""
        lower = text[0].lower() + text[1:]
        if lower.startswith(("verify ", "check ", "validate ", "confirm ", "ensure ")):
            return text[0].upper() + text[1:]
        return f"Verify that {lower}"

    def ensure_sentence(text: str) -> str:
        text = text.strip()
        if not text:
            return ""
        if not text.endswith('.'):
            return f"{text}."
        return text

    def make_actionable_from_criterion(criterion: str) -> str:
        text = criterion.strip().rstrip('.')
        lower = text.lower()

        if lower.startswith("users can "):
            return ensure_sentence(f"Verify that users can {text[10:]}")

        if lower.startswith("user can "):
            return ensure_sentence(f"Verify that users can {text[9:]}")

        if "appears in checkout" in lower:
            return ensure_sentence(text.replace("appears in checkout", "appears as an option in the checkout page"))

        if "remove saved cards" in lower or "delete saved cards" in lower:
            return "Verify that users can remove saved cards from checkout."

        if "saved cards are shown" in lower:
            return "Verify that saved cards are shown correctly."

        if "saved cards" in lower and ("support" in lower or "secure" in lower):
            return "Verify saved cards behavior and secure handling according to the Confluence notes."

        if "payment method x is available only for logged-in users" in lower:
            return "Verify that payment method X is available only for logged-in users."

        if "error is shown" in lower or "invalid data" in lower or lower.startswith("error "):
            return "Enter invalid payment data and verify the correct error message is shown."

        if "required" in lower or "optional" in lower or "validation" in lower:
            return ensure_sentence(normalize_check(text))

        if lower.startswith("payment method") or "payment" in lower or "card" in lower:
            return ensure_sentence(normalize_check(text))

        return ensure_sentence(normalize_check(text))

    checks: List[str] = []
    seen = set()
    description = request.jira_description.lower()
    summary = request.jira_summary.lower()

    def add_check(check: str):
        check = check.strip()
        if not check:
            return
        if check.endswith('.'):
            check = check
        if check not in seen:
            seen.add(check)
            checks.append(check)

    # Summary-based concrete check
    if "payment method" in summary or "payment" in summary or "card" in summary:
        add_check("Review the Jira summary and verify the requested payment method behavior in checkout.")

    # Description-based concrete checks
    if "checkout" in description:
        add_check("Navigate to checkout and verify the new payment method entry points and form fields are visible.")

    if "card" in description or "payment method" in description or "payment" in description:
        add_check("Enter payment details and verify field validation, including which fields are required versus optional.")

    if "invalid" in description or "error" in description:
        add_check("Enter invalid payment data and verify the correct error message is shown.")

    # Acceptance criteria-based concrete checks
    for criterion in request.acceptance_criteria:
        parsed = make_actionable_from_criterion(criterion)
        add_check(parsed)

    # Add required/optional field validation explicitly if not already present
    if ("payment" in description or "card" in description or "checkout" in description) and not any(
        keyword in check.lower()
        for check in checks
        for keyword in ["required", "optional", "validation", "validate"]
    ):
        add_check("Verify which payment fields are required or optional and confirm validation behavior.")

    if request.frontend_changes:
        add_check("Validate the front-end layout and interactions of the new payment fields during checkout.")

    if request.confluence_excerpt:
        add_check(
            "Cross-check Confluence notes to verify the payment flow requirements, saved card behavior, and any environment or data assumptions."
        )
        excerpt_lower = request.confluence_excerpt.lower()
        if "saved cards" in excerpt_lower:
            add_check("Verify saved cards behavior according to the Confluence requirements.")
        if "secure handling" in excerpt_lower or "securely" in excerpt_lower:
            add_check("Verify secure handling of payment data as described in Confluence.")

    if request.additional_context:
        add_check(f"Use additional context when checking edge cases and release constraints: {request.additional_context}")

    if not checks:
        add_check("Verify the functionality described in the Jira issue.")
        add_check("Confirm acceptance criteria are met.")

    if request.frontend_changes and not request.design_available:
        design_note = (
            "Design assets are not available; confirm the exact field layout, labels, and interaction rules with product or design."
        )
    else:
        design_note = "Design information is available or not needed for the current scope."

    plan_lines = [
        f"## Test Plan for {request.jira_key} — {request.jira_summary}",
        "",
        "### Specific checks",
    ]

    for idx, check in enumerate(checks, start=1):
        plan_lines.append(f"{idx}. {check}")

    plan_lines.extend([
        "",
        "### Why these checks matter",
        "- These checks are built from the actual Jira summary, description, and acceptance criteria.",
        "- They focus on concrete page elements, validation rules, and error behavior.",
        "- They help QA verify the exact functionality requested by the task.",
    ])

    if request.frontend_changes:
        plan_lines.extend([
            "",
            "### Front-end and design note",
            f"- {design_note}",
        ])

    plan_lines.extend([
        "",
        "### How to execute",
        "- Follow the user flow described in the Jira task.",
        "- Verify each specific check against the actual UI and behavior.",
        "- Log actual results and compare them to expected behavior.",
        "",
        "### Next step for QA confirmation",
        "- Confirm whether these specific checks cover the functionality and if additional detail is needed.",
    ])

    return TestPlanResponse(
        plan_markdown="\n".join(plan_lines),
        suggested_checks=checks,
        qa_confirm_question=(
            "Please confirm whether these specific checks cover the functionality described in the task "
            "and if any additional detail is needed."
        ),
    )


def load_confluence_text(confluence_excerpt: Optional[str], confluence_file_path: Optional[str]) -> Optional[str]:
    if confluence_file_path:
        base_dir = Path(__file__).resolve().parent
        candidate = (base_dir / confluence_file_path).resolve()
        if base_dir not in candidate.parents and candidate != base_dir:
            raise HTTPException(status_code=400, detail="Invalid confluence_file_path")
        if not candidate.exists():
            raise HTTPException(status_code=400, detail=f"Confluence file not found: {confluence_file_path}")
        return candidate.read_text(encoding="utf-8")
    return confluence_excerpt


@app.post("/generate-test-plan", response_model=TestPlanResponse)
def generate_test_plan(request: TestPlanRequest):
    request.confluence_excerpt = load_confluence_text(request.confluence_excerpt, request.confluence_file_path)
    return build_test_plan(request)


@app.post("/generate-test-plan/plain", response_class=PlainTextResponse)
def generate_test_plan_plain(request: TestPlanRequest):
    request.confluence_excerpt = load_confluence_text(request.confluence_excerpt, request.confluence_file_path)
    result = build_test_plan(request)
    return PlainTextResponse(content=result.plan_markdown, media_type="text/plain")
