#!/usr/bin/env python3
"""
批量为 Markdown front matter 填充 lastmod 字段。

规则：
- 仅处理 content/ 目录下的 .md 文件。
- 已有 lastmod 的文件跳过。
- 使用文件的 mtime（YYYY-MM-DD）作为 lastmod。
- 若 front matter 中存在 date，则将 lastmod 插在 date 行之后；
  否则在 front matter 结尾前补一行 lastmod。
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def update_file(path: Path) -> bool:
  text = path.read_text(encoding="utf-8")
  if not text.lstrip().startswith("---"):
    return False

  parts = text.split("---", 2)
  if len(parts) < 3:
    return False

  prefix, fm, body = parts
  lines = fm.splitlines()

  # 已经有 lastmod 则跳过
  for line in lines:
    if line.strip().startswith("lastmod:"):
      return False

  # 从 mtime 获取日期
  ts = path.stat().st_mtime
  lastmod = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

  new_lines = []
  inserted = False
  for line in lines:
    new_lines.append(line)
    if not inserted and line.strip().startswith("date:"):
      new_lines.append(f"lastmod: {lastmod}")
      inserted = True
  if not inserted:
    new_lines.append(f"lastmod: {lastmod}")

  new_fm = "\n".join(new_lines)
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
  print(f"Updated lastmod in {changed} files.")


if __name__ == "__main__":
  main()

