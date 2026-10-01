from pathlib import Path
import re

PATTERNS = [
    r'(?i)api[_-]?key\s*=\s*["\'][^"\']+["\']',
    r'(?i)password\s*=\s*["\'][^"\']+["\']',
    r'(?i)secret\s*=\s*["\'][^"\']+["\']',
]

SKIP = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}

violations = []

for path in Path(".").rglob("*.py"):
    if any(part in SKIP for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pattern in PATTERNS:
        if re.search(pattern, text):
            violations.append(str(path))

if violations:
    print("POSSIBLE HARDCODED SECRET FOUND:")
    for item in sorted(set(violations)):
        print(f"- {item}")
    raise SystemExit(1)

print("SECRET PATTERN CHECK PASSED")
