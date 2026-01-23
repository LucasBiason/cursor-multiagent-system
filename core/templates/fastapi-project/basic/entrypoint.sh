#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as errors
# Fail on pipeline errors
set -euo pipefail

# Function to display CLI help
cli_help() {
  local cli_name=${0##*/}
  echo "
$cli_name
FastAPI Application - Entrypoint CLI
Usage: $cli_name [command]

Commands:
  dev           Start development server (uvicorn with reload)
  prod          Start production server (uvicorn multi-worker)
  test          Run tests with coverage (90%+ required)
  migrate       Apply database migrations (alembic upgrade head)
  downgrade     Revert last migration (alembic downgrade -1)
  shell         Open Python shell
  health        Check API health and dependencies
  *             Display this help message

Environment Variables:
  PORT          Server port (default: 8000)
  WORKERS       Number of workers for production (default: 4)
  LOG_LEVEL     Logging level (default: info)
  RUN_MIGRATIONS Run migrations on startup (default: false)
"
  exit 1
}

# Function to wait for database
wait_for_db() {
  if [ -z "${DATABASE_URL:-}" ]; then
    echo "⚠️  WARNING: DATABASE_URL not set, skipping database check"
    return 0
  fi
  
  echo "⏳ Waiting for database..."
  # Extract host and port from DATABASE_URL
  # Format: postgresql://user:pass@host:port/dbname
  DB_HOST=$(echo "$DATABASE_URL" | sed -n 's/.*@\([^:]*\):.*/\1/p')
  DB_PORT=$(echo "$DATABASE_URL" | sed -n 's/.*:\([0-9]*\)\/.*/\1/p' || echo "5432")
  
  if [ -n "$DB_HOST" ] && [ -n "$DB_PORT" ]; then
    until nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
      echo "Database is unavailable - sleeping"
      sleep 2
    done
    echo "✅ Database is ready!"
  fi
}

# Function to check dependencies
check_dependencies() {
  echo "🔍 Checking dependencies..."
  
  # Check Python
  if ! command -v python &> /dev/null; then
    echo "❌ ERROR: Python not found"
    exit 1
  fi
  
  # Check uvicorn
  if ! python -c "import uvicorn" 2>/dev/null; then
    echo "❌ ERROR: uvicorn not installed"
    exit 1
  fi
  
  echo "✅ Dependencies OK"
}

# Main command handler
case "${1:-help}" in
  dev)
    echo "========================================="
    echo "FastAPI - DEVELOPMENT MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-8000}
    LOG_LEVEL=${LOG_LEVEL:-debug}
    
    echo "Starting development server..."
    echo "  Port: $PORT"
    echo "  Hot reload: enabled"
    echo "  Log level: $LOG_LEVEL"
    echo "========================================="
    
    wait_for_db
    
    if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
      echo "📦 Running migrations..."
      alembic upgrade head || echo "⚠️  No migrations to run"
    fi
    
    exec uvicorn src.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --reload \
      --log-level "$LOG_LEVEL"
    ;;

  prod|runserver)
    echo "========================================="
    echo "FastAPI - PRODUCTION MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-4}
    LOG_LEVEL=${LOG_LEVEL:-info}
    
    echo "Starting production server..."
    echo "  Port: $PORT"
    echo "  Workers: $WORKERS"
    echo "  Log level: $LOG_LEVEL"
    echo "========================================="
    
    wait_for_db
    
    if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
      echo "📦 Running migrations..."
      alembic upgrade head || echo "⚠️  No migrations to run"
    fi
    
    exec uvicorn src.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --workers "$WORKERS" \
      --log-level "$LOG_LEVEL"
    ;;

  test)
    echo "========================================="
    echo "Running tests with coverage..."
    echo "========================================="
    
    pytest tests/ \
      --cov=src \
      --cov-report=term-missing \
      --cov-report=html \
      --cov-fail-under=90 \
      -v
    ;;

  migrate)
    echo "========================================="
    echo "Running database migrations..."
    echo "========================================="
    
    wait_for_db
    alembic upgrade head
    echo "✅ Migrations applied"
    ;;

  downgrade)
    echo "========================================="
    echo "Reverting last migration..."
    echo "========================================="
    
    wait_for_db
    alembic downgrade -1
    echo "✅ Migration reverted"
    ;;

  shell)
    echo "========================================="
    echo "Opening Python shell..."
    echo "========================================="
    exec python -i
    ;;

  health)
    echo "========================================="
    echo "Health Check"
    echo "========================================="
    check_dependencies
    wait_for_db || echo "⚠️  Database check skipped"
    echo "✅ API is ready to start"
    ;;

  *)
    cli_help
    ;;
esac

