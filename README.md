# Apollo.io MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with the Apollo.io API. This server enables AI assistants to search for accounts, enrich people and organization data, and retrieve contact information.

## Features

### Account Management
- **Search Accounts**: Find companies by name, location, employee count, and industry
- **Get Account Details**: Retrieve comprehensive account information by ID
- **Create Accounts**: Add new accounts to your Apollo.io database
- **Update Accounts**: Modify existing account information

### People & Contact Data
- **Search People**: Find contacts by job title, seniority, company, and location
- **Enrich Person**: Get detailed contact information including emails and phone numbers
- **Bulk Enrichment**: Enrich multiple people or organizations simultaneously

### Organization Data
- **Enrich Organizations**: Get detailed company information from domain
- **Bulk Organization Enrichment**: Enrich up to 10 companies at once
- **Technology Stack**: See what technologies companies use
- **Financial Data**: Access funding information and revenue data

### Additional Features
- **Persona Information**: Access created persona data and counts
- **Intent Data**: Integration ready for Bombora intent data
- **Email Accounts**: Manage email accounts for sequences
- **Opportunities**: Search and manage sales opportunities
- **Health Checks**: Verify API connectivity and authentication

## Prerequisites

- Python 3.8 or higher
- UV package manager
- Apollo.io API key

## Installation

### Quick Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd apollo-mcp
   ```

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Set up your Apollo.io API key**:
   ```bash
   export APOLLO_API_KEY="your_actual_apollo_api_key_here"
   ```

5. **Configure your MCP client** (see Configuration section below)

### Automated Setup

Use the deployment script for easier setup:
```bash
./deploy.sh
```

This will:
- Install UV if needed
- Install dependencies
- Create a `.env` file template
- Run setup verification

## Configuration

### Apollo.io API Key

1. **Get your API key**:
   - Log in to your Apollo.io account
   - Go to Settings → Integrations → API
   - Generate or copy your API key

2. **Set the API key** (choose one method):
   
   **Option A: Environment Variable** (Recommended)
   ```bash
   export APOLLO_API_KEY="your_actual_apollo_api_key_here"
   ```
   
   **Option B: .env File**
   ```bash
   echo "APOLLO_API_KEY=your_actual_apollo_api_key_here" > .env
   ```

### MCP Client Configuration

#### For Claude Desktop

1. **Update the configuration file**:
   - Copy `claude_desktop_config.json` to your Claude Desktop configuration
   - Update the `cwd` path to your actual project directory:
   
   ```json
   {
     "mcpServers": {
       "apollo": {
         "command": "uv",
         "args": ["run", "python", "src/apollo_mcp_server.py"],
         "cwd": "/path/to/your/apollo-mcp",
         "env": {
           "APOLLO_API_KEY": "your_apollo_api_key_here"
         }
       }
     }
   }
   ```

2. **Find your Claude Desktop config location**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

#### For Cursor

1. **Update the Cursor configuration**:
   - The `.cursor/mcp_servers.json` file is already configured
   - Update the `cwd` path to your actual project directory
   - Ensure your `APOLLO_API_KEY` environment variable is set

#### For Other MCP Clients

Use the provided configuration as a template and adapt for your specific client.

### Included Scripts

The repository includes several helper scripts:

- **`run_mcp_server.sh`**: Standard script to run the MCP server
- **`debug_mcp_server.sh`**: Debug version with detailed logging
- **`deploy.sh`**: Automated setup and deployment script

All scripts automatically:
- Detect the correct project directory
- Find UV installation (checks `~/.local/bin` and `~/.cargo/bin`)
- Validate that `APOLLO_API_KEY` is set
- Provide helpful error messages

## Usage

### Running the Server

```bash
uv run python src/apollo_mcp_server.py
```

Or using the installed script:

```bash
uv run apollo-mcp-server
```

### Available Tools

#### Account Search
```python
search_accounts({
    "q_organization_name": "Google",
    "organization_locations": ["California, US"],
    "organization_num_employees_ranges": ["1000,10000"],
    "page": 1,
    "per_page": 25
})
```

#### People Search
```python
search_people({
    "q_organization_domains": "apollo.io\ngoogle.com",
    "person_titles": ["CEO", "CTO", "VP Engineering"],
    "person_seniorities": ["senior", "manager"],
    "organization_locations": ["California, US"],
    "page": 1,
    "per_page": 10
})
```

#### Person Enrichment
```python
enrich_person({
    "first_name": "Tim",
    "last_name": "Zheng",
    "email": "tim@apollo.io",
    "organization_name": "Apollo",
    "domain": "apollo.io",
    "linkedin_url": "http://www.linkedin.com/in/tim-zheng-677ba010",
    "reveal_personal_emails": true,
    "reveal_phone_number": false
})
```

#### Organization Enrichment
```python
enrich_organization({
    "domain": "apollo.io"
})
```

#### Bulk Organization Enrichment
```python
bulk_enrich_organizations([
    "apollo.io",
    "google.com",
    "microsoft.com"
])
```

## API Endpoints Covered

- `/v1/accounts/search` - Account search
- `/v1/accounts/{id}` - Get account by ID  
- `/v1/accounts` - Create/update accounts
- `/v1/mixed_people/search` - People search
- `/v1/people/match` - Person enrichment
- `/api/v1/people/bulk_match` - Bulk people enrichment
- `/v1/organizations/enrich` - Organization enrichment
- `/api/v1/organizations/bulk_enrich` - Bulk organization enrichment
- `/v1/opportunities/search` - Opportunities search
- `/v1/email_accounts` - Email accounts
- `/v1/auth/health` - Health check

## Error Handling

The server includes comprehensive error handling for:
- Invalid API keys
- Rate limiting
- Network errors
- Invalid request parameters
- API response errors

All errors are returned in a structured format with descriptive messages.

## Rate Limiting

Apollo.io has different rate limits for different endpoints:
- Single enrichment endpoints: Standard rate limits
- Bulk enrichment endpoints: 1/10th of standard rate limits
- Search endpoints: Higher rate limits for pagination

The server respects these limits and will return appropriate error messages if limits are exceeded.

## Credit Usage

Different Apollo.io operations consume different types of credits:
- **Email Credits**: 1 credit per verified email found
- **Export Credits**: 1 credit per non-empty record (newer plans)
- **Phone Credits**: Additional charges for phone number reveals

## Development

### Running Tests
```bash
uv run pytest
```

### Code Formatting
```bash
uv run black src/
uv run isort src/
```

### Type Checking
```bash
uv run mypy src/
```

## Documentation

For detailed setup instructions and troubleshooting:
- **[SETUP.md](SETUP.md)** - Complete setup guide with step-by-step instructions
- **[SCRIPTS.md](SCRIPTS.md)** - Documentation for helper scripts
- **[usage_examples.md](usage_examples.md)** - API usage examples and workflows

## Integration with AI Assistants

This MCP server can be used with AI assistants that support the Model Context Protocol, such as:

- Claude Desktop
- Cody
- Continue
- Any MCP-compatible tool

Configure your AI assistant to connect to this server to enable Apollo.io functionality. See [SETUP.md](SETUP.md) for detailed configuration instructions.

## Persona and Intent Data

### Persona Information
The server provides access to persona counts and created persona information through the account and organization endpoints. Persona data helps understand the types of contacts and their roles within organizations.

### Intent Data Integration
While Apollo.io doesn't directly provide Bombora intent data through their standard API, the server is structured to easily integrate intent data when available. This typically requires:

1. Separate Bombora API integration
2. Data correlation between Apollo.io contacts and Bombora intent signals
3. Custom enrichment workflows

Contact Apollo.io support for information about intent data partnerships and availability.

## Support

For issues with this MCP server:
1. Check the error messages and logs
2. Verify your API key is valid
3. Ensure you have sufficient API credits
4. Check Apollo.io API documentation for any changes

For Apollo.io API issues:
- Visit Apollo.io support documentation
- Contact Apollo.io customer support
- Check API status page

## License

MIT License - see LICENSE file for details. 