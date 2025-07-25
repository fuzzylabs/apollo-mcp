#!/usr/bin/env python3
"""
Verification script for Apollo.io MCP Server setup
"""

import os
import sys
from typing import Dict, Any


def verify_imports() -> bool:
    """Verify that all required imports work."""
    try:
        import httpx
        import pydantic
        import fastmcp
        from src.apollo_mcp_server import ApolloAPIClient
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def verify_environment() -> bool:
    """Verify environment setup."""
    if not os.getenv("APOLLO_API_KEY"):
        print("⚠️  APOLLO_API_KEY not set (this is expected for demo)")
        return True
    else:
        print("✅ APOLLO_API_KEY is set")
        return True


def verify_client_creation() -> bool:
    """Verify Apollo API client can be created."""
    try:
        from src.apollo_mcp_server import ApolloAPIClient
        client = ApolloAPIClient("test_key")
        print("✅ Apollo API client can be created")
        return True
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return False


def verify_pydantic_models() -> bool:
    """Verify Pydantic models work correctly."""
    try:
        from src.apollo_mcp_server import (
            AccountSearchRequest,
            PeopleSearchRequest,
            PersonEnrichmentRequest,
            OrganizationEnrichmentRequest
        )
        
        # Test AccountSearchRequest
        account_req = AccountSearchRequest(
            q_organization_name="Google",
            page=1,
            per_page=25
        )
        
        # Test PeopleSearchRequest
        people_req = PeopleSearchRequest(
            q_organization_domains="apollo.io\ngoogle.com",
            person_titles=["CEO", "CTO"],
            page=1
        )
        
        # Test PersonEnrichmentRequest
        person_req = PersonEnrichmentRequest(
            first_name="Tim",
            last_name="Zheng",
            email="tim@apollo.io"
        )
        
        # Test OrganizationEnrichmentRequest
        org_req = OrganizationEnrichmentRequest(domain="apollo.io")
        
        print("✅ All Pydantic models work correctly")
        return True
    except Exception as e:
        print(f"❌ Pydantic model error: {e}")
        return False


def verify_fastmcp_setup() -> bool:
    """Verify FastMCP is set up correctly."""
    try:
        from src.apollo_mcp_server import mcp
        # Just verify that the MCP instance was created successfully
        print(f"✅ FastMCP instance created successfully: {type(mcp).__name__}")
        
        # Verify we can access the app name
        if hasattr(mcp, 'name'):
            print(f"   Server name: {mcp.name}")
        
        # Try to import the decorated functions to ensure they were processed
        expected_functions = [
            "search_accounts",
            "search_people", 
            "enrich_person",
            "enrich_organization",
            "bulk_enrich_organizations",
            "get_account_by_id",
            "create_account",
            "update_account",
            "get_email_accounts",
            "health_check",
            "search_opportunities"
        ]
        
        import src.apollo_mcp_server as server_module
        
        missing_functions = []
        for func_name in expected_functions:
            if not hasattr(server_module, func_name):
                missing_functions.append(func_name)
        
        if missing_functions:
            print(f"❌ Missing tool functions: {missing_functions}")
            return False
        
        print(f"   All {len(expected_functions)} tool functions are available")
        return True
    except Exception as e:
        print(f"❌ FastMCP setup error: {e}")
        return False


def main():
    """Run all verification checks."""
    print("Apollo.io MCP Server Setup Verification")
    print("=" * 40)
    
    checks = [
        ("Imports", verify_imports),
        ("Environment", verify_environment),
        ("Client Creation", verify_client_creation),
        ("Pydantic Models", verify_pydantic_models),
        ("FastMCP Setup", verify_fastmcp_setup),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 40)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All {total} checks passed! Apollo MCP Server is ready to use.")
        print("\nNext steps:")
        print("1. Set your real Apollo.io API key in .env file")
        print("2. Run: uv run python src/apollo_mcp_server.py")
        print("3. Configure your MCP client to connect to this server")
        return 0
    else:
        print(f"❌ {total - passed} checks failed out of {total}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 