#!/usr/bin/env python3
"""
Apollo.io MCP Server

This server provides Model Context Protocol (MCP) tools for interacting with the Apollo.io API.
It supports:
- Account information retrieval and searching
- People information and contact enrichment  
- Organization data enrichment
- Persona information
- Intent data integration
"""

import asyncio
import os
import json
from typing import Any, Dict, List, Optional, Union

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("Apollo.io MCP Server")

# Apollo.io API configuration
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")
APOLLO_BASE_URL = "https://api.apollo.io"

if not APOLLO_API_KEY:
    raise ValueError("APOLLO_API_KEY environment variable is required")


class ApolloAPIClient:
    """Apollo.io API client for making authenticated requests."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = APOLLO_BASE_URL
        self.headers = {
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
            "Cache-Control": "no-cache"
        }
    
    async def make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Apollo.io API."""
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=self.headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=self.headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()


# Initialize Apollo API client
apollo_client = ApolloAPIClient(APOLLO_API_KEY)


# Pydantic models for request/response validation
class AccountSearchRequest(BaseModel):
    """Request model for account search."""
    q_organization_name: Optional[str] = Field(None, description="Company name to search for")
    organization_locations: Optional[List[str]] = Field(None, description="List of locations to filter by")
    organization_num_employees_ranges: Optional[List[str]] = Field(None, description="Employee count ranges")
    industry_tag_ids: Optional[List[str]] = Field(None, description="Industry tag IDs")
    page: int = Field(1, description="Page number for pagination")
    per_page: int = Field(25, description="Number of results per page")


class PeopleSearchRequest(BaseModel):
    """Request model for people search."""
    q_organization_domains: Optional[str] = Field(None, description="Organization domains (newline separated)")
    person_titles: Optional[List[str]] = Field(None, description="Job titles to search for")
    person_seniorities: Optional[List[str]] = Field(None, description="Seniority levels")
    organization_locations: Optional[List[str]] = Field(None, description="Organization locations")
    organization_num_employees_ranges: Optional[List[str]] = Field(None, description="Employee count ranges")
    page: int = Field(1, description="Page number for pagination")
    per_page: int = Field(10, description="Number of results per page")


class PersonEnrichmentRequest(BaseModel):
    """Request model for person enrichment."""
    first_name: Optional[str] = Field(None, description="Person's first name")
    last_name: Optional[str] = Field(None, description="Person's last name")
    email: Optional[str] = Field(None, description="Person's email address")
    organization_name: Optional[str] = Field(None, description="Company name")
    domain: Optional[str] = Field(None, description="Company domain")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    reveal_personal_emails: bool = Field(False, description="Whether to reveal personal emails")
    reveal_phone_number: bool = Field(False, description="Whether to reveal phone numbers")


class OrganizationEnrichmentRequest(BaseModel):
    """Request model for organization enrichment."""
    domain: str = Field(..., description="Company domain to enrich")


# MCP Tools
@mcp.tool()
async def search_accounts(request: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Search for accounts/companies in Apollo.io database.
    
    This tool allows you to search for companies by name, location, employee count,
    and other criteria. Useful for finding potential prospects and account information.
    """
    endpoint = "/v1/accounts/search"
    
    # Handle both JSON string and dict inputs
    if isinstance(request, str):
        try:
            request = json.loads(request)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in request: {str(e)}"}
    
    # Create and validate request object from dictionary
    try:
        account_request = AccountSearchRequest(**request)
    except Exception as e:
        return {"error": f"Invalid request parameters: {str(e)}"}
    
    # Convert request to dict and remove None values
    search_params = {k: v for k, v in account_request.dict().items() if v is not None}
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=search_params)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def search_people(request: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Search for people/contacts in Apollo.io database.
    
    This tool allows you to search for people by job title, seniority, company domain,
    location, and other criteria. Returns contact information and employment details.
    """
    endpoint = "/v1/mixed_people/search"
    
    # Handle both JSON string and dict inputs
    if isinstance(request, str):
        try:
            request = json.loads(request)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in request: {str(e)}"}
    
    # Create and validate request object from dictionary
    try:
        people_request = PeopleSearchRequest(**request)
    except Exception as e:
        return {"error": f"Invalid request parameters: {str(e)}"}
    
    # Convert request to dict and remove None values
    search_params = {k: v for k, v in people_request.dict().items() if v is not None}
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=search_params)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def enrich_person(request: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Enrich a person's information and reveal contact details.
    
    This tool enriches person data and can reveal email addresses and phone numbers.
    The more information provided, the higher the match likelihood.
    """
    endpoint = "/v1/people/match"
    
    # Handle both JSON string and dict inputs
    if isinstance(request, str):
        try:
            request = json.loads(request)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in request: {str(e)}"}
    
    # Create and validate request object from dictionary
    try:
        person_request = PersonEnrichmentRequest(**request)
    except Exception as e:
        return {"error": f"Invalid request parameters: {str(e)}"}
    
    # Convert request to dict and remove None values
    enrich_params = {k: v for k, v in person_request.dict().items() if v is not None}
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=enrich_params)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def enrich_organization(request: Union[Dict[str, Any], str]) -> Dict[str, Any]:
    """
    Enrich organization/company information.
    
    This tool enriches company data based on domain, returning detailed information
    about the organization including industry, employee count, contact info, and more.
    """
    endpoint = "/v1/organizations/enrich"
    
    # Handle both JSON string and dict inputs
    if isinstance(request, str):
        try:
            request = json.loads(request)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in request: {str(e)}"}
    
    # Create and validate request object from dictionary
    try:
        org_request = OrganizationEnrichmentRequest(**request)
    except Exception as e:
        return {"error": f"Invalid request parameters: {str(e)}"}
    
    params = {"domain": org_request.domain}
    
    try:
        result = await apollo_client.make_request("GET", endpoint, params=params)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def bulk_enrich_organizations(domains: List[str]) -> Dict[str, Any]:
    """
    Bulk enrich multiple organizations at once.
    
    This tool enriches multiple companies simultaneously based on their domains.
    Up to 10 domains can be processed in a single request.
    """
    if len(domains) > 10:
        return {"error": "Maximum 10 domains allowed per bulk enrichment request"}
    
    endpoint = "/api/v1/organizations/bulk_enrich"
    data = {"domains": domains}
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=data)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def get_account_by_id(account_id: str) -> Dict[str, Any]:
    """
    Retrieve detailed information for a specific account by ID.
    
    This tool fetches comprehensive account data including contact information,
    custom fields, and associated personas.
    """
    endpoint = f"/v1/accounts/{account_id}"
    
    try:
        result = await apollo_client.make_request("GET", endpoint)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def create_account(
    name: str,
    domain: Optional[str] = None,
    phone_number: Optional[str] = None,
    raw_address: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new account in Apollo.io.
    
    This tool creates a new account with the provided information.
    The domain and address will be intelligently parsed for additional data.
    """
    endpoint = "/v1/accounts"
    
    data = {"name": name}
    if domain:
        data["domain"] = domain
    if phone_number:
        data["phone_number"] = phone_number
    if raw_address:
        data["raw_address"] = raw_address
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=data)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def update_account(
    account_id: str,
    name: Optional[str] = None,
    domain: Optional[str] = None,
    phone_number: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update an existing account in Apollo.io.
    
    This tool updates account information with the provided data.
    Only specified fields will be updated.
    """
    endpoint = f"/v1/accounts/{account_id}"
    
    data = {}
    if name:
        data["name"] = name
    if domain:
        data["domain"] = domain
    if phone_number:
        data["phone_number"] = phone_number
    
    if not data:
        return {"error": "At least one field must be provided for update"}
    
    try:
        result = await apollo_client.make_request("PUT", endpoint, data=data)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def get_email_accounts() -> Dict[str, Any]:
    """
    Retrieve email accounts associated with your Apollo.io account.
    
    This tool returns the list of configured email accounts for sending
    sequences and campaigns.
    """
    endpoint = "/v1/email_accounts"
    
    try:
        result = await apollo_client.make_request("GET", endpoint)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check the health and authentication status of the Apollo.io API connection.
    
    This tool verifies that the API key is valid and the service is accessible.
    """
    endpoint = "/v1/auth/health"
    
    try:
        result = await apollo_client.make_request("GET", endpoint)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


@mcp.tool()
async def search_opportunities(
    page: int = 1,
    per_page: int = 25,
    account_stage_ids: Optional[List[str]] = None,
    sort_by_field: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for opportunities in Apollo.io.
    
    This tool searches for sales opportunities with filtering and sorting options.
    Useful for tracking deals and pipeline management.
    """
    endpoint = "/v1/opportunities/search"
    
    data = {
        "page": page,
        "per_page": per_page
    }
    
    if account_stage_ids:
        data["account_stage_ids"] = account_stage_ids
    if sort_by_field:
        data["sort_by_field"] = sort_by_field
    
    try:
        result = await apollo_client.make_request("POST", endpoint, data=data)
        return result
    except httpx.HTTPStatusError as e:
        return {"error": f"API request failed: {e.response.status_code} {e.response.text}"}
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}


def main():
    """Run the Apollo.io MCP server."""
    mcp.run()


if __name__ == "__main__":
    main() 