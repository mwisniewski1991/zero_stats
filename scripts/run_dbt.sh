#!/usr/bin/env bash
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

ENV_FILE="${ENV_FILE:-$REPO_ROOT/scripts/.env}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: .env not found at $ENV_FILE (copy scripts/.env_example to scripts/.env)" >&2
  exit 1
fi

docker build -f app/dbt/zero_stats/Dockerfile -t zero-stats-dbt .

docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  --env-file "$ENV_FILE" \
  zero-stats-dbt "$@"

exit $?
