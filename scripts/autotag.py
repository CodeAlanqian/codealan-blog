#!/usr/bin/env python3
"""
根据文件路径和内容为文章自动补充语义化 tags。

策略（保守，不删除已有 tag）：
- 遍历 content/ 下所有 .md 文件；
- 解析 front matter，如果已有 tags 列表则在其基础上补充；
- 根据路径关键词和部分内容关键词推断主题，追加相应 tag；
- 最多保留前 6 个去重后的 tag。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def infer_tags(path: Path, body: str) -> list[str]:
    tags: list[str] = []
    lower_path = str(path).lower()

    def add(tag: str) -> None:
        if tag and tag not in tags:
            tags.append(tag)

    # 目录 / 文件名 规则
    if "/docker/" in lower_path or "docker" in path.name.lower():
        add("Docker")
    if "/ros_note/" in lower_path or "ros" in path.name.lower():
        add("ROS")
        add("ROS_NOTE")
    if "/ubuntu/" in lower_path:
        add("Ubuntu")
    if "/vln/" in lower_path or "vln" in path.name.lower():
        add("VLN")
    if "深蓝课程" in str(path):
        add("深蓝课程")
    if "项目" in str(path):
        add("项目")
    if "/gdfy/" in lower_path:
        add("GDFY")
    if "/zotero/" in lower_path:
        add("Zotero")
    if "/latex/" in lower_path or "latex" in path.name.lower():
        add("Latex")
    if "/other/" in lower_path:
        add("Other")
    if "essay" in lower_path:
        add("Essay")
    if "ideas" in lower_path:
        add("ideas")

    # 内容关键词（粗略）
    text = body.lower()
    if "reinforcement learning" in text or "强化学习" in body or "grpo" in text:
        add("RL")
    if "large language model" in text or "大模型" in body or "llm" in text:
        add("LLM")
    if "navigation" in text or "导航" in body:
        add("Navigation")
    if "habitat-sim" in text or "habitat" in text:
        add("Habitat")
    if "nextcloud" in text:
        add("Nextcloud")

    return tags


def parse_front_matter(text: str) -> tuple[str, str, str] | None:
    if not text.lstrip().startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return parts[0], parts[1], parts[2]


def parse_tags(fm: str) -> list[str]:
    lines = fm.splitlines()
    tags: list[str] = []
    in_tags = False
    for line in lines:
        stripped = line.strip()
        if not in_tags and stripped.startswith("tags:"):
            in_tags = True
            continue
        if in_tags:
            if stripped.startswith("-"):
                val = stripped[1:].strip().strip("'\"")
                if val:
                    tags.append(val)
            else:
                break
    return tags


def replace_tags(fm: str, new_tags: list[str]) -> str:
    lines = fm.splitlines()
    out: list[str] = []
    in_tags = False
    removed = False
    for line in lines:
        stripped = line.strip()
        if not in_tags and stripped.startswith("tags:"):
            in_tags = True
            removed = True
            continue
        if in_tags:
            if stripped.startswith("-"):
                continue
            in_tags = False
        out.append(line)
    # 在原有 tags: 块之后或末尾插入新的 tags
    if removed:
        # 在第一行 tags: 之前插入会更复杂，简单做法：附加在末尾
        pass
    out.append("tags:")
    for tag in new_tags:
        out.append(f"- {tag}")
    return "\n".join(out)


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    parsed = parse_front_matter(text)
    if not parsed:
        return False
    prefix, fm, body = parsed
    existing = parse_tags(fm)
    # 去重原有 tag
    base_tags: list[str] = []
    for t in existing:
        if t and t not in base_tags:
            base_tags.append(t)

    inferred = infer_tags(path, body)
    for t in inferred:
        if t not in base_tags:
            base_tags.append(t)

    if not base_tags:
        # 兜底：使用文件名作为一个 tag
        slug = re.sub(r"\.md$", "", path.name)
        base_tags.append(slug)

    # 限制最多 6 个 tag，保持简洁
    base_tags = base_tags[:6]

    new_fm = replace_tags(fm, base_tags)
    new_text = f"{prefix}---\n{new_fm}\n---{body}"
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for md in CONTENT.rglob("*.md"):
        if update_file(md):
            changed += 1
    print(f"Autotag updated {changed} files.")


if __name__ == "__main__":
    main()

