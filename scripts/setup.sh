#!/bin/bash

echo "Setting up Cursor Multiagent System..."
echo ""

# Check if running from correct directory
if [ ! -f "README.md" ]; then
    echo "Error: Please run from project root directory"
    exit 1
fi

# Ensure private submodule exists
if [ ! -d "config/.git" ]; then
    echo "Initializing config submodule..."
    git submodule update --init config
    if [ $? -ne 0 ]; then
        echo "Error: could not initialize config submodule. Run 'git submodule update --init config' manually."
        exit 1
    fi
fi

# Create logs directory
mkdir -p logs

# Ensure Cursor agents link exists
mkdir -p .cursor

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found, skipping Python dependencies"
fi

# Copy example configs if private configs don't exist
echo "Checking configuration files..."

if [ ! -f "config/user-context.md" ]; then
    echo "Creating user-context.md from template..."
    cat > config/user-context.md << 'EOF'
# Private User Context

This file contains sensitive information and is gitignored.

## Personal Information

Name: [YOUR_NAME]
Timezone: [YOUR_TIMEZONE]

## Configure your personal context here
See template for structure.

---

Last Updated: $(date +%Y-%m-%d)
EOF
fi

if [ ! -f "config/config.json" ]; then
    echo "Error: config/config.json not found"
    echo "Please create it from template"
    exit 1
fi

# Create symlink for Cursor
# Link Cursor agents directory to private config (allows per-user overrides)
if [ -d "config/agents" ] && [ ! -L ".cursor/agents" ]; then
    echo "Creating symlink for Cursor agents..."
    ln -sf ../../config/agents .cursor/agents
fi

# Validate configuration
echo ""
echo "Validating configuration..."
if [ -f "scripts/validate.sh" ]; then
    bash scripts/validate.sh
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit config/user-context.md with your information"
echo "2. Edit config/system/infrastructure/notion-ids.json with your Notion IDs"
echo "3. Set NOTION_API_KEY environment variable"
echo "4. Run ./scripts/validate.sh to verify setup"
echo ""


