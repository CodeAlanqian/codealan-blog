#!/usr/bin/env bash

# 启动 AI 代理（ai_server.py），日志输出到 ai_log.log
# 使用方式：
#   chmod +x start_ai.sh
#   ./start_ai.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

LOG_FILE="$SCRIPT_DIR/ai_log.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========= AI proxy restart requested =========" >> "$LOG_FILE"

# 若已存在 ai_server.py 进程，先尝试优雅终止
existing_pids=$(pgrep -f "ai_server.py" || true)
if [[ -n "${existing_pids:-}" ]]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Found existing ai_server.py PIDs: $existing_pids, sending SIGTERM..." >> "$LOG_FILE"
  # shellcheck disable=SC2086
  kill $existing_pids 2>/dev/null || true
  # 等待一小段时间让其退出
  sleep 2
  # 如果还在，强制杀掉
  still_pids=$(pgrep -f "ai_server.py" || true)
  if [[ -n "${still_pids:-}" ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] PIDs still alive after SIGTERM, sending SIGKILL: $still_pids" >> "$LOG_FILE"
    # shellcheck disable=SC2086
    kill -9 $still_pids 2>/dev/null || true
  fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting AI proxy (ai_server.py)..." >> "$LOG_FILE"

# 若需要，可以在这里显式加载 .env（ai_server.py 自身也会尝试读取 .env）
if [[ -f "$SCRIPT_DIR/.env" ]]; then
  # 避免在日志或环境中泄露整个文件内容，只导出当前 shell 所需变量
  # shellcheck disable=SC2046
  export $(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' "$SCRIPT_DIR/.env" | cut -d= -f1)
fi

nohup python3 ai_server.py >> "$LOG_FILE" 2>&1 &

echo "AI proxy started with PID $! (log: $LOG_FILE)"
