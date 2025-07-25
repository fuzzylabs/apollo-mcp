# Apollo.io MCP Server Setup Guide

This guide provides detailed setup instructions for the Apollo.io MCP server.

## Prerequisites

- Python 3.8 or higher
- Apollo.io account with API access
- MCP-compatible client (Claude Desktop, Cursor, etc.)

## Step 1: Repository Setup

### Clone the Repository
```bash
git clone <repository-url>
cd apollo-mcp
```

### Install UV Package Manager

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative: Using pip**
```bash
pip install uv
```

### Install Dependencies
```bash
uv sync
```

## Step 2: Apollo.io API Configuration

### Get Your API Key

1. Log in to [Apollo.io](https://app.apollo.io)
2. Navigate to **Settings** → **Integrations** → **API**
3. Copy your existing API key or generate a new one

### Set Your API Key

**Option A: Environment Variable (Recommended)**

**Linux/macOS:**
```bash
export APOLLO_API_KEY="your_actual_apollo_api_key_here"

# To make it permanent, add to your shell profile:
echo 'export APOLLO_API_KEY="your_actual_apollo_api_key_here"' >> ~/.bashrc
# or ~/.zshrc for zsh users
```

**Windows:**
```cmd
set APOLLO_API_KEY=your_actual_apollo_api_key_here

# To make it permanent:
setx APOLLO_API_KEY "your_actual_apollo_api_key_here"
```

**Option B: .env File**
```bash
echo "APOLLO_API_KEY=your_actual_apollo_api_key_here" > .env
```

## Step 3: MCP Client Configuration

### For Claude Desktop

1. **Locate your Claude Desktop configuration file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

2. **Update the configuration:**
   ```json
   {
     "mcpServers": {
       "apollo": {
         "command": "uv",
         "args": ["run", "python", "src/apollo_mcp_server.py"],
         "cwd": "/absolute/path/to/your/apollo-mcp",
         "env": {
           "APOLLO_API_KEY": "your_apollo_api_key_here"
         }
       }
     }
   }
   ```

3. **Replace `/absolute/path/to/your/apollo-mcp`** with your actual project path:
   ```bash
   pwd  # Run this in your apollo-mcp directory to get the full path
   ```

### For Cursor

1. **Update `.cursor/mcp_servers.json`:**
   ```json
   {
     "mcpServers": {
       "apollo": {
         "command": "uv",
         "args": ["run", "python", "src/apollo_mcp_server.py"],
         "cwd": "/absolute/path/to/your/apollo-mcp",
         "env": {
           "APOLLO_API_KEY": "your_apollo_api_key_here"
         },
         "description": "Apollo.io MCP Server for account, people, and organization data"
       }
     }
   }
   ```

2. **Replace the `cwd` path** with your actual project directory path.

### For Other MCP Clients

Use the configuration above as a template and adapt for your specific client's requirements.

## Step 4: Test Your Setup

### Using the Verification Script
```bash
uv run python verify_setup.py
```

### Manual Testing
```bash
# Test server startup
uv run python src/apollo_mcp_server.py

# Test with debug logging
./debug_mcp_server.sh
```

### Test API Connection
The server should start without errors and you should see a message indicating successful connection to Apollo.io.

## Step 5: Using the Helper Scripts

### run_mcp_server.sh
Standard production script:
```bash
./run_mcp_server.sh
```
- Sets up environment
- Validates API key
- Starts the server

### debug_mcp_server.sh
Debug version with detailed logging:
```bash
./debug_mcp_server.sh
```
- Logs debug information to `cursor_debug.log`
- Helpful for troubleshooting
- Shows environment setup details

### deploy.sh
Automated setup and management:
```bash
# Initial setup
./deploy.sh

# Run the server
./deploy.sh run

# Run tests
./deploy.sh test

# Format code
./deploy.sh format

# Type checking
./deploy.sh check
```

## Troubleshooting

### Common Issues

**1. UV not found:**
```bash
# Check if UV is in PATH
which uv

# Add to PATH if needed (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
```

**2. API Key not set:**
```bash
# Check if environment variable is set
echo $APOLLO_API_KEY

# Set it if missing
export APOLLO_API_KEY="your_api_key_here"
```

**3. Permission denied on scripts:**
```bash
# Make scripts executable
chmod +x run_mcp_server.sh debug_mcp_server.sh deploy.sh
```

**4. Python/UV version issues:**
```bash
# Check versions
python --version
uv --version

# Update if needed
uv self update
```

### Debug Logging

For detailed troubleshooting, check the debug log:
```bash
./debug_mcp_server.sh
tail -f cursor_debug.log
```

### API Issues

**Rate Limiting:**
- Apollo.io has different rate limits for different endpoints
- Bulk operations have lower limits
- Check your account's usage dashboard

**Credit Usage:**
- Email reveals: 1 credit per verified email
- Phone reveals: Additional charges
- Monitor usage to avoid unexpected costs

### Client Configuration Issues

**Path Problems:**
- Always use absolute paths in MCP configurations
- Use `pwd` command to get the correct path
- Avoid spaces or special characters in paths

**Environment Variables:**
- Some clients don't inherit shell environment
- Set API key directly in the configuration file
- Restart the client after configuration changes

## Advanced Configuration

### Custom Python Environment
```bash
# Use specific Python version
uv python pin 3.11

# Create virtual environment manually
uv venv --python 3.11
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
```

### Multiple API Keys
```bash
# For different environments
export APOLLO_API_KEY_PROD="prod_key_here"
export APOLLO_API_KEY_DEV="dev_key_here"
```

### Performance Tuning
- Use bulk endpoints for multiple operations
- Implement request batching in your applications
- Monitor API usage and optimize accordingly

## Getting Help

1. **Check the logs:** `cursor_debug.log` for detailed error information
2. **Verify setup:** Run `uv run python verify_setup.py`
3. **API documentation:** [Apollo.io API Docs](https://apolloio.github.io/apollo-api-docs/)
4. **MCP specification:** [Model Context Protocol](https://spec.modelcontextprotocol.org/)

## Next Steps

After successful setup:
1. Review the API examples in `usage_examples.md`
2. Start with simple queries to test functionality
3. Explore the available tools and endpoints
4. Integrate with your AI assistant workflows 