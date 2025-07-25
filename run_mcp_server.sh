#!/bin/bash

# Apollo MCP Server Wrapper for Cursor
# This script ensures the environment is properly set up

set -e

# Set working directory
cd "/Users/maxmulvey/apollo-mcp"

# Set PATH to include UV
export PATH="/Users/maxmulvey/.local/bin:$PATH"

# Ensure APOLLO_API_KEY is set
export APOLLO_API_KEY="${APOLLO_API_KEY:-MDbkLPBqNdPPymSVEY4XCQ}"

# Run the server
exec /Users/maxmulvey/.local/bin/uv run python src/apollo_mcp_server.py 