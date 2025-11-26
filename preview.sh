#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v hugo >/dev/null 2>&1; then
  echo "未找到 hugo，请先安装 Hugo（建议 Extended 版本）。"
  exit 1
fi

hugo server -D --bind 0.0.0.0 --baseURL http://localhost:1313 "$@"
