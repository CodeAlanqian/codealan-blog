#!/usr/bin/env python3
"""
为 VLN 相关笔记批量补充/修复 tags，确保包含 "VLN"。

作用范围：
- 仅处理 content/obsidian/VLN/ 下的 .md 文件。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "content" / "obsidian" / "VLN"


def ensure_vln_tag(front_matter: str) -> tuple[str, bool]:
    lines = front_matter.splitlines()
    have_tags = any(line.strip().startswith("tags:") for line in lines)
    changed = False

    if have_tags:
        new_lines: list[str] = []
        in_tags = False
        has_vln = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not in_tags and stripped.startswith("tags:"):
                new_lines.append("tags:")
                in_tags = True
                continue
            if in_tags:
                # 仍然在 tags 列表中
                if stripped.startswith("-"):
                    val = stripped[1:].strip().strip("'\"")
                    if val.lower() == "vln":
                        has_vln = True
                    new_lines.append(line)
                    continue
                # tags 列表结束，遇到非缩进行
                if not has_vln:
                    new_lines.append("- VLN")
                    changed = True
                in_tags = False
                new_lines.append(line)
            else:
                new_lines.append(line)

        if in_tags and not has_vln:
            new_lines.append("- VLN")
            changed = True

        return "\n".join(new_lines), changed

    # 没有 tags: 行，插入一个
    new_lines = []
    inserted = False
    for line in lines:
        new_lines.append(line)
        stripped = line.strip()
        if not inserted and (stripped.startswith("draft:") or stripped.startswith("lastmod:") or stripped.startswith("date:")):
            # 尝试在这些字段之后插入
            continue
    # 简单策略：在末尾加一个 tags 块
    new_lines.append("tags:")
    new_lines.append("- VLN")
    changed = True
    return "\n".join(new_lines), changed


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.lstrip().startswith("---"):
        return False
    parts = text.split("---", 2)
    if len(parts) < 3:
        return False
    prefix, fm, body = parts
    new_fm, changed = ensure_vln_tag(fm)
    if not changed:
        return False
    new_text = f"{prefix}---\n{new_fm}\n---{body}"
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    if not TARGET_DIR.exists():
        print("VLN directory not found, skip.")
        return
    for md in TARGET_DIR.rglob("*.md"):
        if update_file(md):
            changed += 1
    print(f"Fixed tags in {changed} VLN files.")


if __name__ == "__main__":
    main()

