#!/usr/bin/env python3
"""
Normalize Obsidian import:
- Keep only Markdown in content/obsidian
- Move非 md 文件到 static/obsidian，保持相对路径
- 重写本地图片/链接路径为 /obsidian/<relative>
"""
import os
import re
import shutil
import urllib.parse
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "content" / "obsidian"
STATIC = Path(__file__).resolve().parent.parent / "static" / "obsidian"


def is_http_or_abs(path: str) -> bool:
    return path.startswith(("http://", "https://", "/"))


def resolve_target(raw: str, current: Path):
    raw = raw.strip()
    if is_http_or_abs(raw):
        return None
    target = (current.parent / raw).resolve()
    try:
        rel = target.relative_to(BASE)
    except ValueError:
        return None
    encoded = "/".join(urllib.parse.quote(part) for part in rel.parts)
    return f"/obsidian/{encoded}"


def rewrite_links(text: str, current: Path) -> str:
    def repl_wiki_img(m):
        raw = m.group(1)
        target = resolve_target(raw, current)
        return f"![]({target})" if target else m.group(0)

    def repl_wiki_link(m):
        raw = m.group(1)
        target = resolve_target(raw, current)
        return f"[{raw}]({target})" if target else m.group(0)

    def repl_md_img(m):
        alt, raw = m.group(1), m.group(2)
        target = resolve_target(raw, current)
        return f"![{alt}]({target})" if target else m.group(0)

    text = re.sub(r"!\[\[([^\]]+)\]\]", repl_wiki_img, text)
    text = re.sub(r"\[\[([^\]]+)\]\]", repl_wiki_link, text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_md_img, text)
    return text


def move_non_md():
    for f in BASE.rglob("*"):
        if f.is_file() and f.suffix.lower() != ".md":
            rel = f.relative_to(BASE)
            dest = STATIC / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(f), str(dest))
    # 清理空目录
    for d in sorted([p for p in BASE.rglob("*") if p.is_dir()], reverse=True):
        if not any(d.iterdir()):
            d.rmdir()


def rewrite_all_md():
    for f in BASE.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        new = rewrite_links(text, f)
        if new != text:
            f.write_text(new, encoding="utf-8")


def main():
    STATIC.mkdir(parents=True, exist_ok=True)
    move_non_md()
    rewrite_all_md()


if __name__ == "__main__":
    main()
