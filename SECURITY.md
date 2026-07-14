# SECURITY / Pre-push checklist

This project handles potentially sensitive product artifacts (Jira/Confluence content). Follow these steps before committing or pushing code:

1. Run the quick secrets scanner:

```bash
python scripts/check_secrets.py
```

- The script performs a best-effort scan for common secret patterns. It is not exhaustive; use it as a first safety net.

2. Use additional tools for deeper scanning (recommended):

- `git-secrets` (AWS Labs) — prevents committing AWS keys.
- `detect-secrets` (Yelp) — pre-commit scan for multiple secret types.

3. Review files manually for any customer-specific data or logs. Ensure you do not commit real customer logs or credentials.

4. If you need to store secrets for development, use environment variables or a secrets manager. Do not hardcode secrets in source files.

5. Configure CI to run an automated secrets scan on PRs and before merges.

If you want, I can add a `pre-commit` hook template and a `requirements.txt` entry for `detect-secrets` to automate these checks.
