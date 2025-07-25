# Helper Scripts Documentation

This document explains the helper scripts included with the Apollo.io MCP server.

## Overview

The repository includes three main helper scripts:
- `run_mcp_server.sh` - Standard production script
- `debug_mcp_server.sh` - Debug version with detailed logging  
- `deploy.sh` - Automated setup and deployment

All scripts are designed to be cross-platform compatible and automatically handle environment setup.

## run_mcp_server.sh

**Purpose:** Standard script to run the MCP server in production mode.

### Features
- Automatically detects the project directory
- Finds UV installation in common locations (`~/.local/bin`, `~/.cargo/bin`)
- Validates that `APOLLO_API_KEY` environment variable is set
- Provides clear error messages for missing dependencies
- Runs the server with minimal output

### Usage
```bash
./run_mcp_server.sh
```

### Environment Setup
The script automatically:
1. Sets `SCRIPT_DIR` to the directory containing the script
2. Changes to the script directory as working directory
3. Adds UV to PATH if found in standard locations
4. Validates API key is set (exits with error if missing)

### Error Handling
- **Missing API Key:** Shows instructions to set `APOLLO_API_KEY`
- **UV Not Found:** Exits with error message
- **Script Permissions:** May need `chmod +x run_mcp_server.sh`

## debug_mcp_server.sh

**Purpose:** Debug version with comprehensive logging for troubleshooting.

### Features
- All features of `run_mcp_server.sh`
- Detailed logging to `cursor_debug.log`
- Environment variable debugging
- Path and dependency verification
- Timestamps for all log entries

### Usage
```bash
./debug_mcp_server.sh
```

### Log File
Creates `cursor_debug.log` in the project directory with:
- Script execution timestamps
- Working directory confirmation
- PATH environment details
- UV location and version
- Python version information
- API key validation (first 10 characters only)
- Server startup messages

### Viewing Logs
```bash
# View the complete log
cat cursor_debug.log

# Follow log in real-time
tail -f cursor_debug.log

# View recent entries
tail -20 cursor_debug.log
```

### Sample Log Output
```
2024-01-15 10:30:00: Starting Apollo MCP Server debug...
2024-01-15 10:30:00: Working directory: /path/to/apollo-mcp
2024-01-15 10:30:00: PATH set to: /home/user/.local/bin:/usr/bin:/bin
2024-01-15 10:30:00: APOLLO_API_KEY is set: MDbkLPBqNd...
2024-01-15 10:30:00: UV found at: /home/user/.local/bin/uv
2024-01-15 10:30:00: Python version: Python 3.11.5
2024-01-15 10:30:00: Starting MCP server...
```

## deploy.sh

**Purpose:** Comprehensive deployment and management script.

### Features
- Automated dependency installation
- Environment validation
- Multiple operational modes
- Development tools integration
- Setup verification

### Usage

#### Initial Setup
```bash
./deploy.sh
```
Performs complete setup:
- Installs UV package manager if needed
- Installs project dependencies with `uv sync`
- Creates `.env` template file
- Runs setup verification

#### Run Server
```bash
./deploy.sh run
```
Starts the MCP server using UV.

#### Run Tests
```bash
./deploy.sh test
```
Executes the setup verification script.

#### Code Formatting
```bash
./deploy.sh format
```
Formats code using:
- `black` for Python code formatting
- `isort` for import sorting

#### Type Checking
```bash
./deploy.sh check
```
Runs `mypy` type checking on the source code.

### UV Installation
If UV is not found, the script automatically installs it using:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Environment File
Creates a `.env` template with:
```
APOLLO_API_KEY=your_apollo_api_key_here
```

## Script Architecture

### Common Features

All scripts share these design principles:

#### Dynamic Path Detection
```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
```
- Uses the script's location as the project root
- Works regardless of where the script is called from
- Ensures relative paths work correctly

#### UV Path Detection
```bash
if [ -f "$HOME/.local/bin/uv" ]; then
    export PATH="$HOME/.local/bin:$PATH"
elif [ -f "$HOME/.cargo/bin/uv" ]; then
    export PATH="$HOME/.cargo/bin:$PATH"
fi
```
- Checks common UV installation locations
- Supports both `pip install uv` and `curl | sh` installations
- Gracefully handles different installation methods

#### API Key Validation
```bash
if [ -z "$APOLLO_API_KEY" ]; then
    echo "ERROR: APOLLO_API_KEY environment variable is not set"
    echo "Please set your Apollo.io API key in the APOLLO_API_KEY environment variable"
    exit 1
fi
```
- Validates API key is set before starting
- Provides clear instructions for setting the key
- Prevents server startup with missing credentials

#### Error Handling
- Uses `set -e` for immediate error exit
- Provides descriptive error messages
- Validates dependencies before execution

### Customization

#### Adding Custom Environment Variables
```bash
# In any script, after the API key validation:
export CUSTOM_VAR="${CUSTOM_VAR:-default_value}"
```

#### Custom UV Path
```bash
# Override UV detection by setting UV_PATH
export UV_PATH="/custom/path/to/uv"
```

#### Custom Python Version
```bash
# Use specific Python version
export UV_PYTHON="python3.11"
```

## Troubleshooting

### Permission Issues
```bash
# Make scripts executable
chmod +x *.sh

# Or individually
chmod +x run_mcp_server.sh debug_mcp_server.sh deploy.sh
```

### Path Issues
```bash
# Check if UV is accessible
which uv

# Manually add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Environment Issues
```bash
# Check environment variables
env | grep APOLLO

# Set API key
export APOLLO_API_KEY="your_key_here"
```

### Script Debugging
```bash
# Run with debug output
bash -x ./run_mcp_server.sh

# Check script syntax
bash -n ./run_mcp_server.sh
```

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Setup Apollo MCP Server
  run: |
    chmod +x deploy.sh
    ./deploy.sh
  env:
    APOLLO_API_KEY: ${{ secrets.APOLLO_API_KEY }}

- name: Run Tests
  run: ./deploy.sh test
```

### Docker Integration
```dockerfile
COPY *.sh ./
RUN chmod +x *.sh && ./deploy.sh
```

## Best Practices

1. **Always use the debug script** when troubleshooting issues
2. **Set API key as environment variable** rather than in config files
3. **Use absolute paths** in MCP client configurations
4. **Check logs regularly** for performance and error monitoring
5. **Keep scripts executable** in version control with `git update-index --chmod=+x *.sh` 