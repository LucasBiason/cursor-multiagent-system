#!/usr/bin/env bash

# ============================================
# Entrypoint Flexível para Django
# ============================================
# 
# Este entrypoint permite executar múltiplos comandos no container.
# Para detalhes completos sobre entrypoints, consulte:
# - Docker Entrypoint Skill: skills/infrastructure/docker-entrypoint/SKILL.md
#
# Uso:
#   docker run myapp dev      # Desenvolvimento
#   docker run myapp prod     # Produção
#   docker run myapp test     # Testes
#   docker run myapp migrate  # Migrations
#   docker run myapp health   # Health check
#
# ============================================

# Exit immediately if a command exits with a non-zero status
# Treat unset variables as errors
# Fail on pipeline errors
set -euo pipefail

# Function to display CLI help
cli_help() {
  local cli_name=${0##*/}
  echo "
$cli_name
Django Application - Entrypoint CLI
Usage: $cli_name [command]

Commands:
  migrate       Apply database migrations (alembic upgrade head)
  test          Run tests with coverage (90%+ required)
  dev           Start development server (Django runserver)
  prod          Start production server (gunicorn)
  runserver     Alias for dev (backward compatibility)
  shell         Open Django shell
  health        Check application health
  *             Display this help message

Environment Variables:
  PORT          Server port (default: 8000)
  WORKERS       Number of workers for production (default: 4)
  TIMEOUT       Request timeout (default: 120)
  RUN_MIGRATIONS Run migrations on startup (default: false)
  WAIT_FOR_DB   Wait for database to be ready (default: false)
"
  exit 1
}

# Function to wait for database (if applicable)
wait_for_db() {
  if [ "${WAIT_FOR_DB:-false}" != "true" ]; then
    return 0
  fi

  if [ -z "${DATABASE_URL:-}" ] && [ -z "${DB_HOST:-}" ]; then
    echo "⚠️  WARNING: DATABASE_URL or DB_HOST not set, skipping database wait"
    return 0
  fi

  echo "⏳ Waiting for database..."
  DB_HOST=${DB_HOST:-localhost}
  DB_PORT=${DB_PORT:-5432}

  if command -v nc &> /dev/null; then
    until nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
      echo "Database is unavailable - sleeping"
      sleep 2
    done
    echo "✅ Database is ready!"
  else
    echo "⚠️  netcat not available, skipping database wait"
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

  # Check Django
  if ! python -c "import django" 2>/dev/null; then
    echo "❌ ERROR: Django not installed"
    exit 1
  fi

  echo "✅ Dependencies OK"
}

# Main command handler
case "${1:-help}" in
  migrate)
    echo "========================================="
    echo "Running database migrations..."
    echo "========================================="
    
    wait_for_db
    
    if command -v python &> /dev/null; then
      python manage.py migrate
      echo "✅ Migrations applied"
    else
      echo "❌ ERROR: Python not found"
      exit 1
    fi
    ;;

  test)
    echo "========================================="
    echo "Running tests with coverage..."
    echo "========================================="
    
    pytest --cov=app \
      --cov-report=term-missing \
      --cov-report=html \
      --cov-fail-under=90 \
      -v
    ;;

  dev|runserver)
    echo "========================================="
    echo "Django - DEVELOPMENT MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-8000}
    echo "Starting development server (Django runserver) on 0.0.0.0:$PORT"
    
    wait_for_db
    
    if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
      echo "📦 Running migrations..."
      python manage.py migrate || echo "⚠️  No migrations to run"
    fi
    
    exec python manage.py runserver 0.0.0.0:$PORT
    ;;

  prod)
    echo "========================================="
    echo "Django - PRODUCTION MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-4}
    TIMEOUT=${TIMEOUT:-120}
    
    echo "Starting production server (gunicorn)..."
    echo "  Port: $PORT"
    echo "  Workers: $WORKERS"
    echo "  Timeout: $TIMEOUT"
    echo "========================================="
    
    wait_for_db
    
    if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
      echo "📦 Running migrations..."
      python manage.py migrate || echo "⚠️  No migrations to run"
    fi
    
    # Detectar wsgi module (tenta src.wsgi, app.wsgi, project.wsgi)
    WSGI_MODULE=${WSGI_MODULE:-}
    if [ -z "$WSGI_MODULE" ]; then
      if [ -f "src/wsgi.py" ]; then
        WSGI_MODULE="src.wsgi:application"
      elif [ -f "app/wsgi.py" ]; then
        WSGI_MODULE="app.wsgi:application"
      else
        echo "❌ ERROR: WSGI module not found. Set WSGI_MODULE environment variable."
        exit 1
      fi
    fi
    
    exec gunicorn "$WSGI_MODULE" \
      --bind 0.0.0.0:$PORT \
      --workers $WORKERS \
      --timeout $TIMEOUT \
      --access-logfile - \
      --error-logfile - \
      --log-level info \
      --worker-class sync
    ;;

  shell)
    echo "========================================="
    echo "Opening Django shell..."
    echo "========================================="
    exec python manage.py shell
    ;;

  health)
    echo "========================================="
    echo "Health check..."
    echo "========================================="
    python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection(); print('✅ Database connection OK')" || exit 1
    echo "✅ Application is healthy"
    ;;

  help|*)
    cli_help
    ;;
esac


