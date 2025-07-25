# Apollo.io MCP Server Usage Examples

This document provides practical examples of how to use the Apollo.io MCP server tools.

## Account Management

### Search for Companies
```python
# Search for technology companies in California
search_accounts({
    "q_organization_name": "Google",
    "organization_locations": ["California, US"],
    "organization_num_employees_ranges": ["1000,50000"],
    "page": 1,
    "per_page": 25
})
```

### Create a New Account
```python
# Add a new company to your Apollo database
create_account(
    name="Acme Corporation",
    domain="acme.com",
    phone_number="1-555-123-4567",
    raw_address="123 Business St, San Francisco, CA 94105"
)
```

### Update Existing Account
```python
# Update company information
update_account(
    account_id="your_account_id",
    name="Updated Company Name",
    phone_number="1-555-987-6543"
)
```

## People Search & Enrichment

### Find Decision Makers
```python
# Search for executives at specific companies
search_people({
    "q_organization_domains": "apollo.io\ngoogle.com\nmicrosoft.com",
    "person_titles": ["CEO", "CTO", "VP Engineering", "Head of Sales"],
    "person_seniorities": ["c_suite", "vp", "director"],
    "organization_locations": ["California, US", "New York, US"],
    "page": 1,
    "per_page": 20
})
```

### Enrich Contact Information
```python
# Get detailed contact info for a specific person
enrich_person({
    "first_name": "Tim",
    "last_name": "Zheng",
    "organization_name": "Apollo",
    "domain": "apollo.io",
    "linkedin_url": "http://www.linkedin.com/in/tim-zheng-677ba010",
    "reveal_personal_emails": true,
    "reveal_phone_number": false  # Set to true if you need phone numbers
})
```

### Find Contacts by Job Function
```python
# Search for marketing professionals
search_people({
    "person_titles": [
        "Marketing Manager", 
        "VP Marketing", 
        "Chief Marketing Officer",
        "Growth Manager"
    ],
    "person_seniorities": ["manager", "senior", "vp"],
    "organization_num_employees_ranges": ["100,10000"],
    "page": 1,
    "per_page": 50
})
```

## Organization Enrichment

### Get Company Details
```python
# Enrich a single company
enrich_organization({
    "domain": "apollo.io"
})
```

### Bulk Company Enrichment
```python
# Enrich multiple companies at once (max 10)
bulk_enrich_organizations([
    "apollo.io",
    "salesforce.com", 
    "hubspot.com",
    "outreach.io",
    "salesloft.com"
])
```

## Prospecting Workflows

### Find Similar Companies
```python
# Step 1: Find a target company profile
target_company = enrich_organization({"domain": "target-company.com"})

# Step 2: Search for similar companies
similar_companies = search_accounts({
    "industry_tag_ids": [target_company["organization"]["industry_tag_id"]],
    "organization_num_employees_ranges": ["100,1000"],
    "organization_locations": ["California, US"],
    "per_page": 50
})
```

### Build Contact Lists
```python
# Step 1: Find target companies
companies = search_accounts({
    "q_organization_name": "SaaS",
    "organization_num_employees_ranges": ["50,500"],
    "organization_locations": ["California, US", "New York, US"]
})

# Step 2: Find decision makers at those companies
domains = [company["domain"] for company in companies["accounts"]]
domain_string = "\n".join(domains[:10])  # Max 10 domains

contacts = search_people({
    "q_organization_domains": domain_string,
    "person_titles": ["CEO", "CTO", "VP Sales", "VP Marketing"],
    "person_seniorities": ["c_suite", "vp"]
})
```

### Lead Qualification
```python
# Step 1: Enrich company
company_data = enrich_organization({"domain": "prospect-company.com"})

# Step 2: Check company fit
if (company_data["organization"]["estimated_num_employees"] >= 100 and 
    "saas" in company_data["organization"]["industry"].lower()):
    
    # Step 3: Find key contacts
    contacts = search_people({
        "q_organization_domains": "prospect-company.com",
        "person_titles": ["CEO", "VP Sales", "Head of Revenue"],
        "person_seniorities": ["c_suite", "vp"]
    })
    
    # Step 4: Enrich contact details
    for person in contacts["people"]:
        enriched = enrich_person({
            "first_name": person["first_name"],
            "last_name": person["last_name"],
            "domain": "prospect-company.com",
            "linkedin_url": person["linkedin_url"],
            "reveal_personal_emails": true
        })
```

## Intent Data Integration

While Apollo.io doesn't directly provide Bombora intent data through their standard API, you can correlate Apollo contacts with intent signals:

```python
# Hypothetical workflow for intent data correlation
def correlate_intent_data(apollo_contacts, bombora_intent_signals):
    """
    Correlate Apollo contact data with Bombora intent signals
    This would require a separate Bombora integration
    """
    enriched_contacts = []
    
    for contact in apollo_contacts:
        # Match by company domain or name
        domain = contact.get("organization", {}).get("primary_domain")
        if domain:
            intent_signals = bombora_intent_signals.get(domain, [])
            contact["intent_signals"] = intent_signals
            
        enriched_contacts.append(contact)
    
    return enriched_contacts
```

## Monitoring & Health Checks

### Verify API Connection
```python
# Check if your API key is working
health_status = health_check()
print(health_status)  # Should return {"is_logged_in": true}
```

### Check Email Account Setup
```python
# Verify email accounts for sequences
email_accounts = get_email_accounts()
print(f"Connected email accounts: {len(email_accounts['email_accounts'])}")
```

## Advanced Search Patterns

### Multi-criteria Prospecting
```python
# Complex search with multiple filters
advanced_search = search_people({
    "q_organization_domains": "technology-companies.com\nsaas-companies.com",
    "person_titles": [
        "VP Sales", "Sales Director", "Head of Sales",
        "VP Marketing", "Marketing Director", "CMO"
    ],
    "person_seniorities": ["vp", "director", "c_suite"],
    "organization_locations": [
        "San Francisco, CA, US",
        "New York, NY, US", 
        "Austin, TX, US",
        "Seattle, WA, US"
    ],
    "organization_num_employees_ranges": ["100,2000"],
    "per_page": 25
})
```

### Geographic Expansion
```python
# Find contacts in new markets
international_prospects = search_people({
    "person_titles": ["Country Manager", "Regional Director", "VP International"],
    "organization_locations": [
        "London, UK",
        "Berlin, Germany",
        "Paris, France",
        "Amsterdam, Netherlands"
    ],
    "organization_num_employees_ranges": ["500,10000"]
})
```

## Error Handling Examples

```python
# Always handle potential API errors
try:
    result = enrich_person({
        "email": "contact@company.com",
        "reveal_personal_emails": true
    })
    
    if "error" in result:
        print(f"API Error: {result['error']}")
    else:
        print(f"Found contact: {result['person']['name']}")
        
except Exception as e:
    print(f"Request failed: {e}")
```

## Rate Limiting Best Practices

- **Single enrichment**: Standard rate limits apply
- **Bulk enrichment**: 1/10th of standard rate limits (use sparingly)
- **Search endpoints**: Higher limits for pagination
- **Always respect rate limits**: Add delays between requests if needed

## Credit Management

- **Email Credits**: 1 credit per verified email found
- **Export Credits**: 1 credit per non-empty record (newer plans)
- **Phone Credits**: Additional charges for phone number reveals

Monitor your credit usage through the Apollo.io dashboard to avoid unexpected charges. 