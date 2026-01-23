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
Node.js Application - Entrypoint CLI
Usage: $cli_name [command]

Commands:
  dev           Start development server (nodemon/ts-node-dev)
  prod          Start production server (node dist/index.js)
  test          Run tests with coverage
  build         Build application (tsc/npm run build)
  seed          Run database seed scripts
  migrate       Run database migrations (if applicable)
  shell         Open Node.js shell
  health        Check service health and dependencies
  *             Display this help message

Environment Variables:
  PORT          Server port (default: 3000)
  NODE_ENV      Node environment (development/production)
  LOG_LEVEL     Logging level (default: info)
"
  exit 1
}

# Function to check dependencies
check_dependencies() {
  echo "🔍 Checking dependencies..."
  
  # Check Node.js
  if ! command -v node &> /dev/null; then
    echo "❌ ERROR: Node.js not found"
    exit 1
  fi
  
  # Check npm
  if ! command -v npm &> /dev/null; then
    echo "❌ ERROR: npm not found"
    exit 1
  fi
  
  # Check if node_modules exists
  if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm ci
  fi
  
  echo "✅ Dependencies OK"
}

# Function to wait for database (if applicable)
wait_for_db() {
  if [ -z "${DATABASE_URL:-}" ] && [ -z "${DB_HOST:-}" ]; then
    return 0
  fi
  
  echo "⏳ Waiting for database..."
  DB_HOST=${DB_HOST:-localhost}
  DB_PORT=${DB_PORT:-5432}
  
  until nc -z "$DB_HOST" "$DB_PORT" 2>/dev/null; do
    echo "Database is unavailable - sleeping"
    sleep 2
  done
  echo "✅ Database is ready!"
}

# Main command handler
case "${1:-help}" in
  dev)
    echo "========================================="
    echo "Node.js - DEVELOPMENT MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-3000}
    NODE_ENV=${NODE_ENV:-development}
    
    echo "Starting development server..."
    echo "  Port: $PORT"
    echo "  Environment: $NODE_ENV"
    echo "  Hot reload: enabled"
    echo "========================================="
    
    wait_for_db
    
    # Use nodemon if available, otherwise ts-node-dev, otherwise node with --watch
    if [ -f "package.json" ] && grep -q "nodemon" package.json; then
      exec npm run dev
    elif [ -f "package.json" ] && grep -q "ts-node-dev" package.json; then
      exec npm run dev
    else
      exec node --watch src/index.js
    fi
    ;;

  prod|runserver)
    echo "========================================="
    echo "Node.js - PRODUCTION MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-3000}
    NODE_ENV=${NODE_ENV:-production}
    
    echo "Starting production server..."
    echo "  Port: $PORT"
    echo "  Environment: $NODE_ENV"
    echo "========================================="
    
    wait_for_db
    
    # Build if dist doesn't exist
    if [ ! -d "dist" ] && [ -f "package.json" ] && grep -q '"build"' package.json; then
      echo "📦 Building application..."
      npm run build
    fi
    
    exec node dist/index.js
    ;;

  test)
    echo "========================================="
    echo "Running tests with coverage..."
    echo "========================================="
    check_dependencies
    
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
      npm test
    else
      echo "⚠️  No test script found in package.json"
      exit 1
    fi
    ;;

  build)
    echo "========================================="
    echo "Building application..."
    echo "========================================="
    check_dependencies
    
    if [ -f "package.json" ] && grep -q '"build"' package.json; then
      npm run build
      echo "✅ Build completed"
    else
      echo "⚠️  No build script found in package.json"
      exit 1
    fi
    ;;

  seed)
    echo "========================================="
    echo "Running seed scripts..."
    echo "========================================="
    check_dependencies
    wait_for_db
    
    if [ -f "package.json" ] && grep -q '"seed"' package.json; then
      npm run seed
    elif [ -f "scripts/seed.js" ]; then
      node scripts/seed.js
    else
      echo "⚠️  No seed script found"
      exit 1
    fi
    ;;

  migrate)
    echo "========================================="
    echo "Running database migrations..."
    echo "========================================="
    check_dependencies
    wait_for_db
    
    if [ -f "package.json" ] && grep -q '"migrate"' package.json; then
      npm run migrate
    elif [ -f "node_modules/.bin/knex" ]; then
      npx knex migrate:latest
    else
      echo "⚠️  No migration tool found"
      exit 1
    fi
    ;;

  shell)
    echo "========================================="
    echo "Opening Node.js shell..."
    echo "========================================="
    exec node -i
    ;;

  health)
    echo "========================================="
    echo "Health Check"
    echo "========================================="
    check_dependencies
    wait_for_db || echo "⚠️  Database check skipped"
    echo "✅ Service is ready"
    ;;

  *)
    cli_help
    ;;
esac

