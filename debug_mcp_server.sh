#!/bin/bash

# Debug Apollo MCP Server Wrapper for Cursor
# This script logs debug information to help troubleshoot

# Create log file
LOG_FILE="/Users/maxmulvey/apollo-mcp/cursor_debug.log"
echo "$(date): Starting Apollo MCP Server debug..." >> "$LOG_FILE"

# Set working directory
cd "/Users/maxmulvey/apollo-mcp"
echo "$(date): Working directory: $(pwd)" >> "$LOG_FILE"

# Set PATH to include UV
export PATH="/Users/maxmulvey/.local/bin:$PATH"
echo "$(date): PATH set to: $PATH" >> "$LOG_FILE"

# Ensure APOLLO_API_KEY is set
export APOLLO_API_KEY="${APOLLO_API_KEY:-MDbkLPBqNdPPymSVEY4XCQ}"
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
exec /Users/maxmulvey/.local/bin/uv run python src/apollo_mcp_server.py 