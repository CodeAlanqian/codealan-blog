#!/usr/bin/env python3
"""
移除所有 Markdown front matter 中的 series 字段。

规则：
- 仅处理 content/ 目录下的 .md 文件。
- 删除从 `series:` 开始的块，直到遇到非缩进行或 front matter 结束。
"""
from __future__ import annotations

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
  new_lines = []
  in_series = False
  changed = False
  for line in lines:
    stripped = line.strip()
    if not in_series and stripped.startswith("series:"):
      in_series = True
      changed = True
      continue
    if in_series:
      # 继续跳过缩进行（如 "- xxx"），直到遇到非缩进行
      if stripped.startswith("-"):
        continue
      # series 块结束，恢复正常处理当前行
      in_series = False
      # 当前行需要正常保留
    new_lines.append(line)
  if not changed:
    return False
  new_fm = "\n".join(new_lines)
  new_text = f"{prefix}---\n{new_fm}\n---{body}"
  path.write_text(new_text, encoding="utf-8")
  return True


def main() -> None:
  changed = 0
  for md in CONTENT.rglob("*.md"):
    if update_file(md):
      changed += 1
  print(f"Removed series from {changed} files.")


if __name__ == "__main__":
  main()

