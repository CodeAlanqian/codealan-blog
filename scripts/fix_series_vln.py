#!/usr/bin/env python3
"""
为 VLN 相关笔记批量添加专栏（series）字段。

规则：
- 仅处理 content/obsidian/VLN/ 下的 md 文件。
- 若已有 series，则不覆盖。
- series 统一设置为 ["VLN课程"]。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR = ROOT / "content" / "obsidian" / "VLN"
SERIES_NAME = "VLN课程"


def update_file(path: Path) -> bool:
  text = path.read_text(encoding="utf-8")
  if not text.lstrip().startswith("---"):
    return False
  parts = text.split("---", 2)
  if len(parts) < 3:
    return False
  prefix, fm, body = parts
  lines = fm.splitlines()
  # 已有 series 则跳过
  for line in lines:
    if line.strip().startswith("series:"):
      return False
  new_lines = []
  inserted = False
  for line in lines:
    new_lines.append(line)
    if not inserted and line.strip().startswith("tags:"):
      # 在 tags 之后插入 series
      new_lines.append("series:")
      new_lines.append(f"- {SERIES_NAME}")
      inserted = True
  if not inserted:
    new_lines.append("series:")
    new_lines.append(f"- {SERIES_NAME}")
  new_fm = "\n".join(new_lines)
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
  print(f"Updated series for {changed} VLN files.")


if __name__ == "__main__":
  main()
