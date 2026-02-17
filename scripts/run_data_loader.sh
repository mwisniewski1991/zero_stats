#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

ENV_FILE="${ENV_FILE:-$REPO_ROOT/app/data_loader/.env}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env not found at $ENV_FILE" >&2
  exit 1
fi

docker build -f app/data_loader/Dockerfile -t zero-stats-data-loader app/data_loader

docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  --env-file "$ENV_FILE" \
  zero-stats-data-loader

exit $?
