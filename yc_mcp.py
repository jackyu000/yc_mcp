from mcp.server.fastmcp import FastMCP
import requests
import traceback
import sys

# Create the server
mcp = FastMCP("YC Directory Server")

@mcp.tool()
def list_top_companies(limit: int = 10) -> dict:
    """
    List the top YC companies.
    
    Args:
        limit: Maximum number of companies to return
        
    Returns:
        Dictionary with list of top companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/top.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data[:limit]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_company_details(slug: str) -> dict:
    """
    Fetch company data by slug (e.g., "airbnb").
    
    Args:
        slug: The company identifier
        
    Returns:
        Company details
    """
    try:
        url = f"https://yc-oss.github.io/api/companies/{slug}.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_companies_by_batch(batch: str) -> dict:
    """
    Query companies from a specific YC batch.
    
    Args:
        batch: The YC batch identifier (e.g., "W21")
        
    Returns:
        Dictionary with companies from the specified batch
    """
    try:
        url = f"https://yc-oss.github.io/api/batches/{batch.lower()}.json"
        response = requests.get(url)
        response.raise_for_status()
        return {"batch": batch, "companies": response.json()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_companies(keyword: str) -> dict:
    """
    Search for companies with a keyword in name/description.
    
    Args:
        keyword: The search term to look for in company names and descriptions
        
    Returns:
        Dictionary of matching companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        all_companies = response.json()
        matches = [c for c in all_companies if keyword.lower() in c['name'].lower() or keyword.lower() in c.get('one_liner', '').lower()]
        return {"matches": matches}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def compare_company_sizes(slug1: str, slug2: str) -> dict:
    """
    Compare team_size of two companies.
    
    Args:
        slug1: First company identifier
        slug2: Second company identifier
        
    Returns:
        Comparison result
    """
    try:
        c1 = get_company_details(slug1)
        c2 = get_company_details(slug2)
        if "error" in c1 or "error" in c2:
            return {"error": f"Failed to fetch details. {c1.get('error')} {c2.get('error')}"}
        size1 = c1.get("team_size", 0)
        size2 = c2.get("team_size", 0)
        comparison = f"{slug1} ({size1}) vs {slug2} ({size2})"
        return {"comparison": comparison}
    except Exception as e:
        return {"error": str(e)}

@mcp.resource("yc://company/{slug}")
def company_resource(slug: str) -> dict:
    """
    Resource representation for a YC company.
    
    Args:
        slug: The company identifier
        
    Returns:
        Resource representation with company summary
    """
    result = get_company_details(slug)
    if "error" in result:
        return result
    return {
        "summary": f"{result['name']}: {result.get('one_liner', 'No one-liner')}"
    }

# Metadata tools
@mcp.tool()
def get_api_metadata() -> dict:
    """
    Get metadata about the YC API, including counts of companies, batches, industries, and tags.
    
    Returns:
        Dictionary with API metadata
    """
    try:
        url = "https://yc-oss.github.io/api/meta.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Companies collection tools
@mcp.tool()
def list_all_companies() -> dict:
    """
    List all launched YC companies.
    
    Returns:
        Dictionary with all companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_black_founded_companies() -> dict:
    """
    List Black-founded YC companies.
    
    Returns:
        Dictionary with Black-founded companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/black-founded.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_hispanic_latino_founded_companies() -> dict:
    """
    List Hispanic/Latino-founded YC companies.
    
    Returns:
        Dictionary with Hispanic/Latino-founded companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/hispanic-latino-founded.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_women_founded_companies() -> dict:
    """
    List women-founded YC companies.
    
    Returns:
        Dictionary with women-founded companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/women-founded.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_nonprofit_companies() -> dict:
    """
    List not-for-profit YC companies.
    
    Returns:
        Dictionary with not-for-profit companies
    """
    try:
        url = "https://yc-oss.github.io/api/companies/nonprofit.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_hiring_companies() -> dict:
    """
    List YC companies currently hiring.
    
    Returns:
        Dictionary with companies that are currently hiring
    """
    try:
        url = "https://yc-oss.github.io/api/companies/hiring.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

# Industry tools
@mcp.tool()
def list_companies_by_industry(industry: str) -> dict:
    """
    List companies in a specific industry.
    
    Args:
        industry: The industry identifier (e.g., "fintech", "healthcare", "b2b")
        
    Returns:
        Dictionary with companies in the specified industry
    """
    try:
        # Convert spaces to hyphens and make lowercase for API compatibility
        industry_slug = industry.lower().replace(" ", "-")
        url = f"https://yc-oss.github.io/api/industries/{industry_slug}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"industry": industry, "companies": data}
    except Exception as e:
        return {"error": str(e)}

# Tag tools
@mcp.tool()
def list_companies_by_tag(tag: str) -> dict:
    """
    List companies with a specific tag.
    
    Args:
        tag: The tag identifier (e.g., "ai", "saas", "fintech")
        
    Returns:
        Dictionary with companies having the specified tag
    """
    try:
        # Convert spaces to hyphens and make lowercase for API compatibility
        tag_slug = tag.lower().replace(" ", "-")
        url = f"https://yc-oss.github.io/api/tags/{tag_slug}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"tag": tag, "companies": data}
    except Exception as e:
        return {"error": str(e)}

# Advanced comparison and analytics tools
@mcp.tool()
def compare_companies_by_batch(batch1: str, batch2: str) -> dict:
    """
    Compare companies from two different YC batches.
    
    Args:
        batch1: First batch identifier (e.g., "W21")
        batch2: Second batch identifier (e.g., "S22")
        
    Returns:
        Comparison statistics between the two batches
    """
    try:
        batch1_data = list_companies_by_batch(batch1)
        batch2_data = list_companies_by_batch(batch2)
        
        if "error" in batch1_data or "error" in batch2_data:
            return {"error": f"Failed to fetch batch data. {batch1_data.get('error')} {batch2_data.get('error')}"}
            
        batch1_companies = batch1_data.get("companies", [])
        batch2_companies = batch2_data.get("companies", [])
        
        # Get statistics
        batch1_count = len(batch1_companies)
        batch2_count = len(batch2_companies)
        
        # Calculate industry distributions
        batch1_industries = {}
        batch2_industries = {}
        
        for company in batch1_companies:
            industry = company.get("industry", "Unknown")
            batch1_industries[industry] = batch1_industries.get(industry, 0) + 1
            
        for company in batch2_companies:
            industry = company.get("industry", "Unknown")
            batch2_industries[industry] = batch2_industries.get(industry, 0) + 1
        
        return {
            "comparison": f"{batch1} ({batch1_count} companies) vs {batch2} ({batch2_count} companies)",
            "batch1": {
                "name": batch1,
                "count": batch1_count,
                "industries": batch1_industries
            },
            "batch2": {
                "name": batch2,
                "count": batch2_count,
                "industries": batch2_industries
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def filter_companies(keyword: str = None, industry: str = None, batch: str = None, tag: str = None, limit: int = 50) -> dict:
    """
    Apply multiple filters to find companies matching specific criteria.
    
    Args:
        keyword: Optional keyword to search in company names and descriptions
        industry: Optional industry filter
        batch: Optional batch filter
        tag: Optional tag filter
        limit: Maximum number of results to return
        
    Returns:
        Dictionary with filtered companies
    """
    try:
        all_companies_data = list_all_companies()
        if "error" in all_companies_data:
            return all_companies_data
            
        all_companies = all_companies_data.get("companies", [])
        filtered_companies = all_companies
        
        filters_applied = []
        
        # Apply keyword filter
        if keyword:
            filtered_companies = [c for c in filtered_companies if 
                                  keyword.lower() in c.get('name', '').lower() or 
                                  keyword.lower() in c.get('one_liner', '').lower() or
                                  keyword.lower() in c.get('long_description', '').lower()]
            filters_applied.append(f"keyword='{keyword}'")
        
        # Apply industry filter
        if industry:
            filtered_companies = [c for c in filtered_companies if 
                                  industry.lower() in [i.lower() for i in c.get('industries', [])]]
            filters_applied.append(f"industry='{industry}'")
        
        # Apply batch filter
        if batch:
            filtered_companies = [c for c in filtered_companies if 
                                 batch.lower() == c.get('batch', '').lower()]
            filters_applied.append(f"batch='{batch}'")
        
        # Apply tag filter
        if tag:
            filtered_companies = [c for c in filtered_companies if 
                                tag.lower() in [t.lower() for t in c.get('tags', [])]]
            filters_applied.append(f"tag='{tag}'")
        
        # Apply limit
        filtered_companies = filtered_companies[:limit]
        
        return {
            "filters": filters_applied,
            "total_matches": len(filtered_companies),
            "companies": filtered_companies
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_industry_stats() -> dict:
    """
    Get statistics about industries across all YC companies.
    
    Returns:
        Dictionary with industry statistics
    """
    try:
        all_companies_data = list_all_companies()
        if "error" in all_companies_data:
            return all_companies_data
            
        all_companies = all_companies_data.get("companies", [])
        
        # Count companies by industry
        industry_counts = {}
        for company in all_companies:
            for industry in company.get("industries", ["Unknown"]):
                industry_counts[industry] = industry_counts.get(industry, 0) + 1
        
        # Sort industries by count (descending)
        sorted_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_companies": len(all_companies),
            "industry_stats": {
                industry: count for industry, count in sorted_industries
            }
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_tag_stats() -> dict:
    """
    Get statistics about tags across all YC companies.
    
    Returns:
        Dictionary with tag statistics
    """
    try:
        all_companies_data = list_all_companies()
        if "error" in all_companies_data:
            return all_companies_data
            
        all_companies = all_companies_data.get("companies", [])
        
        # Count companies by tag
        tag_counts = {}
        for company in all_companies:
            for tag in company.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Sort tags by count (descending)
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "total_companies": len(all_companies),
            "tag_stats": {
                tag: count for tag, count in sorted_tags
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Stock data integration for public companies
@mcp.tool()
def get_public_company_stock_info(slug: str) -> dict:
    """
    Get stock information for a public YC company.
    
    Args:
        slug: The company identifier
        
    Returns:
        Dictionary with company details and stock information if available
    """
    try:
        # First get company details
        company_data = get_company_details(slug)
        if "error" in company_data:
            return company_data
            
        # Check if the company is public
        if company_data.get("status") != "Public":
            return {"error": f"{company_data.get('name')} is not a public company"}
            
        # For demonstration purposes, we'd integrate with a stock API here
        # In a real implementation, you would call a stock data API with the company's ticker
        # This is a placeholder that returns mock data
        return {
            "company": company_data.get("name"),
            "status": "Public",
            "stock_info": {
                "note": "This is simulated stock data for demonstration purposes",
                "price": "$XXX.XX",
                "change": "+/-X.XX%",
                "market_cap": "$XX.XX billion"
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Resources for various API entities
@mcp.resource("yc://industry/{industry}")
def industry_resource(industry: str) -> dict:
    """
    Resource representation for a YC industry.
    
    Args:
        industry: The industry identifier
        
    Returns:
        Resource representation with industry summary
    """
    result = list_companies_by_industry(industry)
    if "error" in result:
        return result
    
    companies = result.get("companies", [])
    return {
        "summary": f"Industry: {industry} - {len(companies)} companies",
        "count": len(companies)
    }

@mcp.resource("yc://tag/{tag}")
def tag_resource(tag: str) -> dict:
    """
    Resource representation for a YC tag.
    
    Args:
        tag: The tag identifier
        
    Returns:
        Resource representation with tag summary
    """
    result = list_companies_by_tag(tag)
    if "error" in result:
        return result
    
    companies = result.get("companies", [])
    return {
        "summary": f"Tag: {tag} - {len(companies)} companies",
        "count": len(companies)
    }

@mcp.resource("yc://batch/{batch}")
def batch_resource(batch: str) -> dict:
    """
    Resource representation for a YC batch.
    
    Args:
        batch: The batch identifier (e.g., "W21")
        
    Returns:
        Resource representation with batch summary
    """
    result = list_companies_by_batch(batch)
    if "error" in result:
        return result
    
    companies = result.get("companies", [])
    return {
        "summary": f"Batch: {batch} - {len(companies)} companies",
        "count": len(companies)
    }

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)