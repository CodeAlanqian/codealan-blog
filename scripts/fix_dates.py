#!/usr/bin/env python3
"""
Update front matter dates for existing Markdown content:
- Only touch files whose `date:` is the placeholder 2025-11-26
- Prefer date parsed from filename like 2025.10.31XXX.md / 2025-10-31XXX.md
- Fallback to filesystem mtime (YYYY-MM-DD)
"""
from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PLACEHOLDER = "2025-11-26"

DATE_IN_NAME_RE = re.compile(
    r"(20\d{2})[.\-](\d{1,2})[.\-](\d{1,2})"
)


def parse_date_from_name(path: Path) -> str | None:
    m = DATE_IN_NAME_RE.search(path.stem)
    if not m:
        m = DATE_IN_NAME_RE.search(str(path.parent))
    if not m:
        return None
    y, mo, d = map(int, m.groups())
    try:
        return datetime(y, mo, d).strftime("%Y-%m-%d")
    except ValueError:
        return None


def date_from_mtime(path: Path) -> str:
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        return False

    parts = text.split("---", 2)
    if len(parts) < 3:
        return False

    prefix, fm, body = parts
    lines = fm.splitlines()
    new_lines = []
    old_date = None

    for line in lines:
        if line.strip().startswith("date:"):
            old_date = line.split(":", 1)[1].strip().strip('"').strip("'")
        new_lines.append(line)

    if old_date != PLACEHOLDER:
        return False

    # Decide new date
    new_date = parse_date_from_name(path) or date_from_mtime(path)

    updated_lines = []
    replaced = False
    for line in new_lines:
        if not replaced and line.strip().startswith("date:"):
            updated_lines.append(f'date: {new_date}')
            replaced = True
        else:
            updated_lines.append(line)

    new_fm = "\n".join(updated_lines)
    new_text = f"{prefix}---\n{new_fm}\n---{body}"
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for md in CONTENT.rglob("*.md"):
        if md.name == "_index.md":
            continue
        if update_file(md):
            changed += 1
    print(f"Updated dates in {changed} files.")


if __name__ == "__main__":
    main()

