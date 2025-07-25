#!/bin/bash

# Debug Apollo MCP Server Wrapper for Cursor
# This script logs debug information to help troubleshoot

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create log file
LOG_FILE="$SCRIPT_DIR/cursor_debug.log"
echo "$(date): Starting Apollo MCP Server debug..." >> "$LOG_FILE"

# Set working directory
cd "$SCRIPT_DIR"
echo "$(date): Working directory: $(pwd)" >> "$LOG_FILE"

# Set PATH to include UV (check common installation paths)
if [ -f "$HOME/.local/bin/uv" ]; then
    export PATH="$HOME/.local/bin:$PATH"
elif [ -f "$HOME/.cargo/bin/uv" ]; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi
echo "$(date): PATH set to: $PATH" >> "$LOG_FILE"

# Ensure APOLLO_API_KEY is set (without a default key)
if [ -z "$APOLLO_API_KEY" ]; then
    echo "$(date): ERROR: APOLLO_API_KEY environment variable is not set" >> "$LOG_FILE"
    echo "Please set your Apollo.io API key in the APOLLO_API_KEY environment variable"
    exit 1
fi
echo "$(date): APOLLO_API_KEY is set: ${APOLLO_API_KEY:0:10}..." >> "$LOG_FILE"

# Check UV is available
if command -v uv &> /dev/null; then
    echo "$(date): UV found at: $(which uv)" >> "$LOG_FILE"
else
    echo "$(date): ERROR: UV not found in PATH" >> "$LOG_FILE"
    exit 1
fi

# Check Python/virtual env
echo "$(date): Python version: $(python --version)" >> "$LOG_FILE"

# Run the server
echo "$(date): Starting MCP server..." >> "$LOG_FILE"
exec uv run python src/apollo_mcp_server.py 