#!/bin/bash

echo "Validating Cursor Multiagent System configuration..."
echo ""

ERRORS=0

# Check required files
echo "Checking required files..."

FILES=(
    "config/config.json"
    "config/agents/personal-assistant.mdc"
    "config/agents/studies-coach.mdc"
    "config/agents/work-coach.mdc"
    "config/agents/social-media-coach.mdc"
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

if [ ! -f "config/private/notion-ids.json" ]; then
    echo "WARNING: Missing config/private/notion-ids.json"
    echo "  Create this file with your Notion database IDs"
    ERRORS=$((ERRORS + 1))
fi

if [ ! -f "config/private/user-context.md" ]; then
    echo "WARNING: Missing config/private/user-context.md"
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
    
    if [ -f "config/private/notion-ids.json" ]; then
        jq empty config/private/notion-ids.json 2>/dev/null
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



