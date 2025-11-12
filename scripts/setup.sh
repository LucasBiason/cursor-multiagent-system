#!/bin/bash

echo "Setting up Cursor Multiagent System..."
echo ""

# Check if running from correct directory
if [ ! -f "README.md" ]; then
    echo "Error: Please run from project root directory"
    exit 1
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p config/private
mkdir -p logs
mkdir -p .cursor/agents

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

if [ ! -f "config/private/user-context.md" ]; then
    echo "Creating user-context.md from template..."
    cat > config/private/user-context.md << 'EOF'
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
if [ ! -L ".cursor/agents" ]; then
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
echo "1. Edit config/private/user-context.md with your information"
echo "2. Edit config/private/notion-ids.json with your Notion IDs"
echo "3. Set NOTION_API_KEY environment variable"
echo "4. Run ./scripts/validate.sh to verify setup"
echo ""
