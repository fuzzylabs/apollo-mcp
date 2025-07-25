#!/bin/bash

# Apollo MCP Server Wrapper for Cursor
# This script ensures the environment is properly set up

set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set working directory
cd "$SCRIPT_DIR"

# Set PATH to include UV (check common installation paths)
if [ -f "$HOME/.local/bin/uv" ]; then
    export PATH="$HOME/.local/bin:$PATH"
elif [ -f "$HOME/.cargo/bin/uv" ]; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Ensure APOLLO_API_KEY is set (without a default key)
if [ -z "$APOLLO_API_KEY" ]; then
    echo "ERROR: APOLLO_API_KEY environment variable is not set"
    echo "Please set your Apollo.io API key in the APOLLO_API_KEY environment variable"
    exit 1
fi

# Run the server
exec uv run python src/apollo_mcp_server.py 