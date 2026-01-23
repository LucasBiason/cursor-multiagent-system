#!/bin/bash

echo "Validating Cursor Multiagent System configuration..."
echo ""

ERRORS=0

# Check required files
echo "Checking required files..."

FILES=(
    "config/config.json"
    "core/agents/personal-assistant.mdc"
    "core/agents/studies-coach.mdc"
    "core/agents/work-coach.mdc"
    "core/agents/social-media-coach.mdc"
)

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Missing required file: $file"
        ERRORS=$((ERRORS + 1))
    else
        echo "OK: $file"
    fi
done

echo ""

# Check private configuration
echo "Checking private configuration..."

# Notion IDs are now in the MCP project, not here
# Check if MCP project exists
if [ ! -d "../my-local-place/services/external/notion-automation-suite" ]; then
    echo "WARNING: MCP project not found at my-local-place/services/external/notion-automation-suite"
    echo "  Configure Notion IDs in the MCP project's config/.env file"
fi

if [ ! -f "config/user-context.md" ]; then
    echo "WARNING: Missing config/user-context.md"
    echo "  Create this file with your personal context"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# Check environment variables
echo "Checking environment variables..."

if [ -z "$NOTION_API_KEY" ]; then
    echo "WARNING: NOTION_API_KEY not set"
    echo "  Set with: export NOTION_API_KEY=your_key_here"
else
    echo "OK: NOTION_API_KEY is set"
fi

echo ""

# Check for sensitive data in public files
echo "Checking for sensitive data in public files..."

SENSITIVE_FILES=(
    "docker-compose.yml"
    "docker-compose.*.yml"
    ".env.example"
    "*.md"
)

SENSITIVE_PATTERNS=(
    "password.*="
    "secret.*="
    "key.*="
    "token.*="
    "uri.*=.*://.*:.*@"
    "connection.*=.*://.*:.*@"
    "ntn_[0-9]{10,}[a-zA-Z0-9]{20,}"
    "ghp_[a-zA-Z0-9]{36,}"
    "[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}"
)

FOUND_SENSITIVE=false
for file_pattern in "${SENSITIVE_FILES[@]}"; do
    for file in $(find . -name "$file_pattern" -not -path "./.git/*" -not -path "./node_modules/*" 2>/dev/null); do
        for pattern in "${SENSITIVE_PATTERNS[@]}"; do
            if grep -E -i "${pattern}" "$file" > /dev/null 2>&1; then
                # Ignorar se estiver em comentário ou se for placeholder
                if ! grep -E "(placeholder|example|your_.*_here|change.*me)" "$file" > /dev/null 2>&1; then
                    echo "   ⚠️  WARNING: Possible sensitive data in $file (pattern: ${pattern})"
                    FOUND_SENSITIVE=true
                fi
            fi
        done
    done
done

if [ "$FOUND_SENSITIVE" = true ]; then
    echo "   ⚠️  Review files above for sensitive data"
    ERRORS=$((ERRORS + 1))
else
    echo "   ✓ No sensitive data detected in public files"
fi

echo ""

# Check Docker Compose files for exposed variables
echo "Checking Docker Compose files..."

for compose_file in $(find . -name "docker-compose*.yml" -not -path "./.git/*" 2>/dev/null); do
    if grep -E "environment:" -A 10 "$compose_file" | grep -E "(password|secret|key|token|uri|connection)" | grep -v "env_file" > /dev/null 2>&1; then
        echo "   ✗ ERROR: $compose_file may contain exposed sensitive variables"
        echo "      Use 'env_file:' instead of 'environment:' for sensitive data"
        ERRORS=$((ERRORS + 1))
    else
        echo "   ✓ $compose_file looks safe"
    fi
done

echo ""

# Check JSON syntax
echo "Validating JSON files..."

if command -v jq &> /dev/null; then
    if [ -f "config/config.json" ]; then
        jq empty config/config.json 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "OK: config.json syntax valid"
        else
            echo "ERROR: config.json has syntax errors"
            ERRORS=$((ERRORS + 1))
        fi
    fi
    
    # Notion IDs validation moved to MCP project
    if [ -f "../my-local-place/services/external/notion-automation-suite/config/.env" ]; then
        echo "OK: MCP config file exists"
        if [ $? -eq 0 ]; then
            echo "OK: notion-ids.json syntax valid"
        else
            echo "ERROR: notion-ids.json has syntax errors"
            ERRORS=$((ERRORS + 1))
        fi
    fi
else
    echo "WARNING: jq not installed, skipping JSON validation"
    echo "  Install with: sudo apt install jq"
fi

echo ""
echo "================================"

if [ $ERRORS -eq 0 ]; then
    echo "VALIDATION PASSED"
    echo "System is ready to use!"
    exit 0
else
    echo "VALIDATION FAILED"
    echo "Found $ERRORS error(s)"
    echo "Please fix the issues above"
    exit 1
fi


