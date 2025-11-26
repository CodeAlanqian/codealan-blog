#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_CONTENT="${ROOT_DIR}/content"
TARGET_STATIC="${ROOT_DIR}/static"

mkdir -p "$TARGET_CONTENT" "$TARGET_STATIC"

TMP_DIR=""
cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
}
trap cleanup EXIT

# 支持两种来源：
# 1) 本地 OneDrive 路径（默认 ~/onedrive），可通过 ONEDRIVE_PATH 覆盖
# 2) 共享链接/zip 下载：设置 ONEDRIVE_ZIP_URL（可用 OneDrive 分享链接加 download=1）

if [ -n "${ONEDRIVE_ZIP_URL:-}" ]; then
  echo "Detected ONEDRIVE_ZIP_URL，开始下载..."
  TMP_DIR="$(mktemp -d /tmp/onedrive_sync.XXXXXX)"
  ZIP_FILE="${TMP_DIR}/onedrive.zip"
  if command -v curl >/dev/null 2>&1; then
    curl -L "$ONEDRIVE_ZIP_URL" -o "$ZIP_FILE"
  else
    wget -O "$ZIP_FILE" "$ONEDRIVE_ZIP_URL"
  fi
  unzip -o "$ZIP_FILE" -d "$TMP_DIR"
  # 若解压出来包含一层目录，尝试进入第一层
  FIRST_SUB="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d | head -n1)"
  if [ -n "$FIRST_SUB" ]; then
    ONEDRIVE_PATH="$FIRST_SUB"
  else
    ONEDRIVE_PATH="$TMP_DIR"
  fi
else
  ONEDRIVE_PATH="${ONEDRIVE_PATH:-"$HOME/onedrive"}"
fi

SOURCE_CONTENT="${ONEDRIVE_PATH}/content"
SOURCE_STATIC="${ONEDRIVE_PATH}/static"

echo "Using OneDrive path: ${ONEDRIVE_PATH}"

has_content_dir=false
has_static_dir=false
[ -d "$SOURCE_CONTENT" ] && has_content_dir=true
[ -d "$SOURCE_STATIC" ] && has_static_dir=true

copy_dir() {
  local src="$1"
  local dst="$2"
  local name="$3"
  if [ -d "$src" ]; then
    echo "Syncing ${name}..."
    rsync -av --delete "$src"/ "$dst"/
  else
    echo "Skip ${name}: ${src} 不存在（请在 OneDrive 创建并放置内容）"
  fi
}

copy_dir "$SOURCE_CONTENT" "$TARGET_CONTENT" "content"
copy_dir "$SOURCE_STATIC" "$TARGET_STATIC" "static"

if [ "$has_content_dir" = false ] && [ "$has_static_dir" = false ]; then
  echo "未发现 content/static 目录，启用兼容模式：同步整个目录到 content/obsidian/，排除 .obsidian 和 .git，不影响已有示例内容。"
DEST_OBS="${TARGET_CONTENT}/obsidian"
  mkdir -p "$DEST_OBS"
  rsync -av --delete \
    --exclude ".obsidian" \
    --exclude ".git" \
    --exclude ".DS_Store" \
    "$ONEDRIVE_PATH"/ "$DEST_OBS"/
  chmod -R u+rw "$DEST_OBS"
  # 将非 md 文件（图片等）复制到 static/obsidian/ 以便直接引用
  STATIC_OBS="${TARGET_STATIC}/obsidian"
  mkdir -p "$STATIC_OBS"
  find "$DEST_OBS" -type f ! -name "*.md" -print0 | while IFS= read -r -d '' f; do
    rel="${f#$DEST_OBS/}"
    dest="${STATIC_OBS}/${rel}"
    mkdir -p "$(dirname "$dest")"
    cp -f "$f" "$dest"
  done
  # 给没有 front matter 的笔记自动添加 title 和统一日期
  DEFAULT_DATE="$(date +%F)"
  find "$DEST_OBS" -type f -name "*.md" -print0 | while IFS= read -r -d '' f; do
    first_line="$(head -n1 "$f" || true)"
    if [ "$first_line" = "---" ]; then
      continue
    fi
    title="$(basename "$f" .md)"
    tmp="${f}.tmp"
    {
      echo "---"
      echo "title: \"${title}\""
      echo "date: ${DEFAULT_DATE}"
      echo "draft: false"
      echo "---"
      cat "$f"
    } > "$tmp" && mv "$tmp" "$f"
  done
  # 将 Obsidian wiki 链接转换为标准 Markdown 链接/图片，前缀 /obsidian/；清理 front matter 中的 http url
  PYBIN=""
  for c in python3 python; do
    if command -v "$c" >/dev/null 2>&1; then PYBIN="$c"; break; fi
  done
  if [ -n "$PYBIN" ]; then
    "$PYBIN" - "$DEST_OBS" <<'PY'
import re, urllib.parse, sys
from pathlib import Path

root = Path(sys.argv[1])
for f in root.rglob("*.md"):
    text = f.read_text(encoding="utf-8")
    rel_dir = f.parent.relative_to(root)
    def resolve_path(raw):
        raw = raw.strip()
        if raw.startswith(("http://", "https://", "/")):
            return raw
        return str((rel_dir / raw).as_posix())
    def repl_img(m):
        raw = m.group(1).strip()
        resolved = resolve_path(raw)
        return f"![](/obsidian/{urllib.parse.quote(resolved, safe='/')})"
    def repl_link(m):
        raw = m.group(1).strip()
        resolved = resolve_path(raw)
        return f"[{raw}](/obsidian/{urllib.parse.quote(resolved, safe='/')})"
    new = re.sub(r"!\[\[([^\]]+)\]\]", repl_img, text)
    new = re.sub(r"\[\[([^\]]+)\]\]", repl_link, new)
    # 处理标准 Markdown 图片链接，前缀 /obsidian/（跳过 http/https 和以 / 开头）
    def repl_md_img(m):
        alt = m.group(1)
        path = m.group(2).strip()
        if path.startswith(("http://", "https://", "/")):
            return m.group(0)
        resolved = resolve_path(path)
        enc = urllib.parse.quote(resolved, safe="/")
        return f"![{alt}](/obsidian/{enc})"
    new = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl_md_img, new)
    # 清理 front matter 的 url 字段中 http/https
    new = re.sub(r'^(url:\s*")https?[^"]*(")', r'\1\2', new, flags=re.MULTILINE)
    if new != text:
        f.write_text(new, encoding="utf-8")
PY
  else
    echo "警告：未找到 python3/python，跳过 wiki 链接转换"
  fi
fi

echo "Done. 内容已同步到本地 Hugo 目录。"
