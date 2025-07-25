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

1. **Clone or create the project**:
   ```bash
   mkdir apollo-mcp-server
   cd apollo-mcp-server
   ```

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Apollo.io API key
   ```

## Configuration

### Apollo.io API Key

1. Log in to your Apollo.io account
2. Go to Settings → Integrations → API
3. Generate or copy your API key
4. Add it to your `.env` file:
   ```
   APOLLO_API_KEY=your_actual_api_key_here
   ```

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

## Integration with AI Assistants

This MCP server can be used with AI assistants that support the Model Context Protocol, such as:

- Claude Desktop
- Cody
- Continue
- Any MCP-compatible tool

Configure your AI assistant to connect to this server to enable Apollo.io functionality.

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