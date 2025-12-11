#!/usr/bin/env bash

set -euo pipefail

cli_help() {
  local cli_name=${0##*/}
  echo "
$cli_name
System entrypoint CLI
Usage: $cli_name [command]
Commands:
  migrate       Apply database migrations
  test          Run tests with coverage
  dev           Start development server (Django runserver)
  prod          Start production server (gunicorn)
  runserver     Alias for dev (backward compatibility)
  *             Display this help message
"
  exit 1
}

case "${1:-}" in
  migrate)
    python manage.py migrate
    ;;
  test)
    pytest --cov-report term-missing --cov=app --cov-config=app/.coveragerc tests/ -s
    ;;
  dev|runserver)
    PORT=${PORT:-8000}
    echo "Starting development server (Django runserver) on 0.0.0.0:$PORT"
    exec python manage.py runserver 0.0.0.0:$PORT
    ;;
  prod)
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-4}
    TIMEOUT=${TIMEOUT:-120}

    exec gunicorn src.wsgi:application \
      --bind 0.0.0.0:$PORT \
      --workers $WORKERS \
      --timeout $TIMEOUT \
      --access-logfile - \
      --error-logfile - \
      --log-level info
    ;;
  *)
    cli_help
    ;;
esac


