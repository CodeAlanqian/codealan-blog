#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$ROOT_DIR/copyparty/.env"
COMPOSE_FILE="$ROOT_DIR/docker-compose.copyparty.yml"

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing $ENV_FILE"
  echo "Create it from copyparty/.env.example and set COPYPARTY_ADMIN_PASSWORD."
  exit 1
fi

mkdir -p "$ROOT_DIR/copyparty/files" "$ROOT_DIR/copyparty/state"

docker compose --env-file "$ENV_FILE" -f "$COMPOSE_FILE" up -d
