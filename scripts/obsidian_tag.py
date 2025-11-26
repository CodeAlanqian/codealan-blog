#!/usr/bin/env python3
"""
Enrich tags for obsidian markdown files based on their folder path.
Rules:
- Preserve existing tags; append path-derived tags (unique, in order).
- Path tags: every folder under content/obsidian (excluding the filename), e.g.
  content/obsidian/VLN/深蓝课程/项目/foo.md -> ["VLN", "深蓝课程", "项目"].
"""
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parent.parent / "content" / "obsidian"

def collect_tags(path: Path):
    try:
        rel = path.relative_to(BASE)
    except ValueError:
        return []
    # exclude filename
    parts = rel.parts[:-1]
    # remove empty
    tags = [p for p in parts if p]
    return tags

def main():
    for md in BASE.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        _, fm_text, body = parts
        try:
            data = yaml.safe_load(fm_text) or {}
        except Exception:
            continue
        existing = data.get("tags") or []
        if isinstance(existing, str):
            existing = [existing]
        path_tags = collect_tags(md)
        merged = []
        seen = set()
        for t in list(existing) + path_tags:
            if not t:
                continue
            if t in seen:
                continue
            merged.append(t)
            seen.add(t)
        if not merged:
            continue
        data["tags"] = merged
        new_fm = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
        md.write_text(f"---\n{new_fm}\n---{body}", encoding="utf-8")

if __name__ == "__main__":
    main()
