#!/bin/bash

# Apollo.io MCP Server Deployment Script
# This script helps set up and run the Apollo.io MCP server

set -e

echo "🚀 Apollo.io MCP Server Deployment"
echo "=================================="

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "✅ UV is available"

# Sync dependencies
echo "📚 Installing dependencies..."
uv sync

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file..."
    echo "APOLLO_API_KEY=your_apollo_api_key_here" > .env
    echo "📝 Please edit .env file and add your real Apollo.io API key"
fi

# Run verification
echo "🔍 Running setup verification..."
if uv run python verify_setup.py; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file and set your Apollo.io API key:"
    echo "   APOLLO_API_KEY=your_actual_api_key_here"
    echo ""
    echo "2. Run the server:"
    echo "   ./deploy.sh run"
    echo ""
    echo "3. Or run in development mode:"
    echo "   uv run python src/apollo_mcp_server.py"
    echo ""
    echo "4. Configure your MCP client (e.g., Claude Desktop):"
    echo "   Use the configuration in claude_desktop_config.json"
else
    echo "❌ Setup verification failed. Please check the errors above."
    exit 1
fi

# Handle command line arguments
if [ "$1" = "run" ]; then
    echo "🏃 Starting Apollo.io MCP Server..."
    uv run python src/apollo_mcp_server.py
elif [ "$1" = "test" ]; then
    echo "🧪 Running tests..."
    uv run python verify_setup.py
elif [ "$1" = "format" ]; then
    echo "🎨 Formatting code..."
    uv run black src/ tests/
    uv run isort src/ tests/
elif [ "$1" = "check" ]; then
    echo "🔍 Running type checks..."
    uv run mypy src/
fi 