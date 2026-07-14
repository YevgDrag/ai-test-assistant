#!/usr/bin/env python3
"""Simple repository secrets scanner for quick pre-push checks.

Usage: python scripts/check_secrets.py
Exits with code 0 if no potential secrets found, 1 otherwise.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', '.venv', '.idea', '.vscode', 'node_modules'}
TEXT_EXTS = {'.py', '.md', '.txt', '.json', '.yaml', '.yml', '.ini', '.cfg', '.env'}

PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), 'AWS Access Key ID (AKIA...)'),
    (re.compile(r"(?:aws|AWS)_secret(?:_access)?_key"), 'Possible AWS secret key field name'),
    (re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|PRIVATE) KEY-----"), 'Private key block'),
    (re.compile(r"password\s*=\s*['\"]?\w+['\"]?", re.IGNORECASE), 'Hardcoded password assignment'),
    (re.compile(r"api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9-_]{16,}['\"]?", re.IGNORECASE), 'API key-like string'),
    (re.compile(r"token\s*[:=]\s*['\"]?[A-Za-z0-9-_.]{16,}['\"]?", re.IGNORECASE), 'Token-like string'),
]

findings = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    # prune excluded dirs
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for fname in filenames:
        _, ext = os.path.splitext(fname)
        if ext and ext.lower() not in TEXT_EXTS:
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fh:
                for i, line in enumerate(fh, start=1):
                    for pattern, label in PATTERNS:
                        if pattern.search(line):
                            findings.append((fpath, i, label, line.strip()))
        except Exception:
            # skip binary or unreadable files
            continue

if findings:
    print('\nPotential secrets found:')
    for fpath, lineno, label, snippet in findings:
        print(f'- {fpath}:{lineno} -> {label} -- {snippet}')
    print('\nPlease remove sensitive data and re-run the scanner before push.')
    sys.exit(1)
else:
    print('No obvious secrets found by quick scan.')
    sys.exit(0)
