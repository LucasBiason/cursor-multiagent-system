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
React Application - Entrypoint CLI
Usage: $cli_name [command]

Commands:
  dev           Start development server (Vite/Next.js dev)
  build         Build application for production
  prod          Serve production build (nginx or serve)
  test          Run tests
  lint          Run linter
  health        Check service health
  *             Display this help message

Environment Variables:
  PORT          Server port (default: 3000)
  NODE_ENV      Node environment (development/production)
  VITE_API_URL  API URL for Vite (if using Vite)
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

# Detect framework (Vite, Next.js, Create React App)
detect_framework() {
  if [ -f "vite.config.js" ] || [ -f "vite.config.ts" ]; then
    echo "vite"
  elif [ -f "next.config.js" ] || [ -f "next.config.ts" ]; then
    echo "nextjs"
  elif [ -f "package.json" ] && grep -q "react-scripts" package.json; then
    echo "cra"
  else
    echo "unknown"
  fi
}

# Main command handler
case "${1:-help}" in
  dev)
    echo "========================================="
    echo "React - DEVELOPMENT MODE"
    echo "========================================="
    check_dependencies
    
    PORT=${PORT:-3000}
    NODE_ENV=${ENVIRONMENT:-development}
    
    FRAMEWORK=$(detect_framework)
    echo "Detected framework: $FRAMEWORK"
    echo "Starting development server..."
    echo "  Port: $PORT"
    echo "  Environment: $NODE_ENV"
    echo "========================================="
    
    case "$FRAMEWORK" in
      vite)
        exec npm run dev -- --port "$PORT" --host
        ;;
      nextjs)
        PORT=$PORT exec npm run dev
        ;;
      cra)
        PORT=$PORT exec npm start
        ;;
      *)
        echo "⚠️  Unknown framework, trying npm run dev"
        exec npm run dev
        ;;
    esac
    ;;

  build)
    echo "========================================="
    echo "Building React application..."
    echo "========================================="
    check_dependencies
    
    FRAMEWORK=$(detect_framework)
    echo "Detected framework: $FRAMEWORK"
    
    if [ -f "package.json" ] && grep -q '"build"' package.json; then
      npm run build
      echo "✅ Build completed in dist/ or build/"
    else
      echo "⚠️  No build script found in package.json"
      exit 1
    fi
    ;;

  prod|runserver)
    echo "========================================="
    echo "React - PRODUCTION MODE"
    echo "========================================="
    
    FRAMEWORK=$(detect_framework)
    BUILD_DIR=""
    
    case "$FRAMEWORK" in
      vite)
        BUILD_DIR="dist"
        ;;
      nextjs)
        BUILD_DIR=".next"
        ;;
      cra)
        BUILD_DIR="build"
        ;;
      *)
        BUILD_DIR="dist"
        ;;
    esac
    
    # Check if build exists
    if [ ! -d "$BUILD_DIR" ]; then
      echo "⚠️  Build not found in $BUILD_DIR, building..."
      check_dependencies
      npm run build
    fi
    
    PORT=${PORT:-3000}
    
    echo "Serving production build..."
    echo "  Port: $PORT"
    echo "  Build directory: $BUILD_DIR"
    echo "========================================="
    
    # Use serve if available, otherwise nginx
    if command -v serve &> /dev/null; then
      exec serve -s "$BUILD_DIR" -l "$PORT"
    elif [ -f "/etc/nginx/nginx.conf" ]; then
      # Nginx is available (in container)
      exec nginx -g "daemon off;"
    else
      echo "⚠️  No serve or nginx found, installing serve..."
      npm install -g serve
      exec serve -s "$BUILD_DIR" -l "$PORT"
    fi
    ;;

  test)
    echo "========================================="
    echo "Running tests..."
    echo "========================================="
    check_dependencies
    
    if [ -f "package.json" ] && grep -q '"test"' package.json; then
      npm test
    else
      echo "⚠️  No test script found in package.json"
      exit 1
    fi
    ;;

  lint)
    echo "========================================="
    echo "Running linter..."
    echo "========================================="
    check_dependencies
    
    if [ -f "package.json" ] && grep -q '"lint"' package.json; then
      npm run lint
    else
      echo "⚠️  No lint script found in package.json"
      exit 1
    fi
    ;;

  health)
    echo "========================================="
    echo "Health Check"
    echo "========================================="
    check_dependencies
    echo "✅ Service is ready"
    ;;

  *)
    cli_help
    ;;
esac

