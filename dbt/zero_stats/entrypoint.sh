#!/usr/bin/env bash
set -e

DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-postgres}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_SCHEMA="${DB_SCHEMA:-zero_stats}"

mkdir -p ~/.dbt
cat > ~/.dbt/profiles.yml << EOF
zero_stats:
  target: dev
  outputs:
    dev:
      type: postgres
      host: $DB_HOST
      port: $DB_PORT
      dbname: $DB_NAME
      user: $DB_USER
      password: "$DB_PASSWORD"
      schema: $DB_SCHEMA
      threads: 4
EOF

exec dbt "$@"
