#!/usr/bin/env python3
"""
Auto-append tags to obsidian markdown files based on simple keyword matching.
Rules:
- Preserve existing tags, append matched tags (unique).
- Keywords are matched case-insensitively in full text.
"""
from pathlib import Path
import yaml

BASE = Path(__file__).resolve().parent.parent / "content" / "obsidian"

TAG_RULES = {
    "VLN": ["vln", "导航", "airvln", "vision-language navigation", "vla"],
    "RL": ["强化学习", "rl", "grpo", "policy gradient", "value function"],
    "Docker": ["docker", "容器"],
    "ROS": ["ros", "colcon", "ros2", "rviz"],
    "Zotero": ["zotero", "文献"],
    "Latex": ["latex", "xelatex"],
    "Essay": ["essay", "英语", "english essay"],
    "Security": ["安全", "security", "火绒"],
    "Git": ["git", "github"],
    "Ubuntu": ["ubuntu", "linux"],
    "LLM": ["llm", "deepseek", "chatgpt", "大模型"],
}


def match_tags(text: str):
    found = set()
    lower = text.lower()
    for tag, keywords in TAG_RULES.items():
        for kw in keywords:
            if kw.lower() in lower:
                found.add(tag)
                break
    return list(found)


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
        content_part = body.lower()
        auto = match_tags(content_part)
        merged = []
        seen = set()
        for t in existing + auto:
            if not t or t in seen:
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
