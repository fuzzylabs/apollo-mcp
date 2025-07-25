"""
Tests for Apollo.io MCP Server
"""

import pytest
import os
from unittest.mock import AsyncMock, patch
import httpx

from src.apollo_mcp_server import ApolloAPIClient, apollo_client


class TestApolloAPIClient:
    """Test cases for Apollo API client."""
    
    def test_client_initialization(self):
        """Test that the client initializes correctly."""
        client = ApolloAPIClient("test_api_key")
        assert client.api_key == "test_api_key"
        assert client.base_url == "https://api.apollo.io"
        assert client.headers["X-Api-Key"] == "test_api_key"
    
    @pytest.mark.asyncio
    async def test_make_request_get(self):
        """Test GET request functionality."""
        client = ApolloAPIClient("test_api_key")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"test": "data"})
            mock_response.raise_for_status = AsyncMock()
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await client.make_request("GET", "/test")
            assert result == {"test": "data"}
    
    @pytest.mark.asyncio
    async def test_make_request_post(self):
        """Test POST request functionality."""
        client = ApolloAPIClient("test_api_key")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value={"success": True})
            mock_response.raise_for_status = AsyncMock()
            
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await client.make_request("POST", "/test", data={"key": "value"})
            assert result == {"success": True}
    
    @pytest.mark.asyncio
    async def test_make_request_http_error(self):
        """Test handling of HTTP errors."""
        client = ApolloAPIClient("test_api_key")
        
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.raise_for_status = AsyncMock(side_effect=httpx.HTTPStatusError(
                "Error", request=None, response=mock_response
            ))
            
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(httpx.HTTPStatusError):
                await client.make_request("GET", "/test")


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check tool."""
    from src.apollo_mcp_server import health_check
    
    with patch.object(apollo_client, 'make_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"is_logged_in": True}
        
        # Access the underlying function from the FunctionTool wrapper
        result = await health_check.func()
        assert result == {"is_logged_in": True}
        mock_request.assert_called_once_with("GET", "/v1/auth/health")


@pytest.mark.asyncio
async def test_search_accounts():
    """Test the account search tool."""
    from src.apollo_mcp_server import search_accounts
    
    with patch.object(apollo_client, 'make_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"accounts": [{"name": "Google"}]}
        
        # Access the underlying function from the FunctionTool wrapper
        result = await search_accounts.func(
            q_organization_name="Google",
            page=1,
            per_page=25
        )
        assert result == {"accounts": [{"name": "Google"}]}
        mock_request.assert_called_once()


@pytest.mark.asyncio
async def test_enrich_organization():
    """Test the organization enrichment tool."""
    from src.apollo_mcp_server import enrich_organization
    
    with patch.object(apollo_client, 'make_request', new_callable=AsyncMock) as mock_request:
        mock_request.return_value = {"organization": {"name": "Apollo.io"}}
        
        # Access the underlying function from the FunctionTool wrapper
        result = await enrich_organization.func(domain="apollo.io")
        assert result == {"organization": {"name": "Apollo.io"}}
        mock_request.assert_called_once_with("GET", "/v1/organizations/enrich", params={"domain": "apollo.io"})


@pytest.mark.asyncio
async def test_bulk_enrich_organizations_limit():
    """Test that bulk enrichment respects the 10 domain limit."""
    from src.apollo_mcp_server import bulk_enrich_organizations
    
    domains = [f"domain{i}.com" for i in range(11)]  # 11 domains
    
    # Access the underlying function from the FunctionTool wrapper
    result = await bulk_enrich_organizations.func(domains)
    assert "error" in result
    assert "Maximum 10 domains" in result["error"]


if __name__ == "__main__":
    pytest.main([__file__]) 