from mcp.server.fastmcp import FastMCP
import requests
import traceback
import sys
import datetime

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

# Additional company list endpoints
@mcp.tool()
def list_black_founded_companies() -> dict:
    """
    List companies founded by Black entrepreneurs.
    
    Returns:
        Dictionary with list of Black-founded companies
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
    List companies founded by Hispanic or Latino entrepreneurs.
    
    Returns:
        Dictionary with list of Hispanic/Latino-founded companies
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
    List companies founded by women entrepreneurs.
    
    Returns:
        Dictionary with list of women-founded companies
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
    List not-for-profit companies in YC.
    
    Returns:
        Dictionary with list of non-profit companies
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
    List companies that are currently hiring.
    
    Returns:
        Dictionary with list of companies currently hiring
    """
    try:
        url = "https://yc-oss.github.io/api/companies/hiring.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"companies": data}
    except Exception as e:
        return {"error": str(e)}

# Industry-related tools
@mcp.tool()
def list_industries() -> dict:
    """
    List all available industries in the YC database.
    
    Returns:
        Dictionary with list of all industries
    """
    try:
        url = "https://yc-oss.github.io/api/meta.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"industries": data.get("industries", [])}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_companies_by_industry(industry: str) -> dict:
    """
    List companies in a specific industry.
    
    Args:
        industry: The industry name (e.g., "Consumer", "B2B")
        
    Returns:
        Dictionary with list of companies in the specified industry
    """
    try:
        # URL encode the industry name for the path
        import urllib.parse
        encoded_industry = urllib.parse.quote(industry.lower())
        url = f"https://yc-oss.github.io/api/industries/{encoded_industry}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"industry": industry, "companies": data}
    except Exception as e:
        return {"error": str(e)}

# Tag-related tools
@mcp.tool()
def list_tags() -> dict:
    """
    List all available tags in the YC database.
    
    Returns:
        Dictionary with list of all tags
    """
    try:
        url = "https://yc-oss.github.io/api/meta.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"tags": data.get("tags", [])}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_companies_by_tag(tag: str) -> dict:
    """
    List companies with a specific tag.
    
    Args:
        tag: The tag name (e.g., "AI", "Marketplace")
        
    Returns:
        Dictionary with list of companies with the specified tag
    """
    try:
        # URL encode the tag name for the path
        import urllib.parse
        encoded_tag = urllib.parse.quote(tag.lower())
        url = f"https://yc-oss.github.io/api/tags/{encoded_tag}.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {"tag": tag, "companies": data}
    except Exception as e:
        return {"error": str(e)}

# Metadata tool
@mcp.tool()
def get_api_metadata() -> dict:
    """
    Get metadata about the YC API including counts and last updated timestamp.
    
    Returns:
        Dictionary with API metadata
    """
    try:
        url = "https://yc-oss.github.io/api/meta.json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Convert the timestamp to a readable format
        timestamp = data.get("last_updated", 0)
        if timestamp:
            last_updated = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_updated = "Unknown"
            
        return {
            "last_updated": last_updated,
            "companies_count": data.get("companies_count", 0),
            "batches_count": data.get("batches_count", 0),
            "industries_count": data.get("industries_count", 0),
            "tags_count": data.get("tags_count", 0)
        }
    except Exception as e:
        return {"error": str(e)}

# Stage filter tool
@mcp.tool()
def filter_companies_by_stage(stage: str) -> dict:
    """
    Filter companies by their growth stage.
    
    Args:
        stage: The company stage (e.g., "Seed", "Growth", "Public")
        
    Returns:
        Dictionary with list of companies at the specified stage
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        all_companies = response.json()
        
        # Filter companies by stage (case-insensitive)
        stage_lower = stage.lower()
        filtered_companies = [c for c in all_companies if c.get("stage", "").lower() == stage_lower]
        
        return {"stage": stage, "companies": filtered_companies}
    except Exception as e:
        return {"error": str(e)}

# Region filter tool
@mcp.tool()
def filter_companies_by_region(region: str) -> dict:
    """
    Filter companies by their region/location.
    
    Args:
        region: The region name (e.g., "United States", "Europe")
        
    Returns:
        Dictionary with list of companies in the specified region
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        all_companies = response.json()
        
        # Filter companies by region (substring match, case-insensitive)
        region_lower = region.lower()
        filtered_companies = []
        for company in all_companies:
            regions = company.get("regions", [])
            if any(region_lower in r.lower() for r in regions):
                filtered_companies.append(company)
                
        return {"region": region, "companies": filtered_companies}
    except Exception as e:
        return {"error": str(e)}

# Team size comparison tool
@mcp.tool()
def list_companies_by_team_size(min_size: int, max_size: int = None) -> dict:
    """
    List companies within a specific team size range.
    
    Args:
        min_size: Minimum team size
        max_size: Maximum team size (optional)
        
    Returns:
        Dictionary with list of companies in the specified team size range
    """
    try:
        url = "https://yc-oss.github.io/api/companies/all.json"
        response = requests.get(url)
        response.raise_for_status()
        all_companies = response.json()
        
        # Filter companies by team size
        if max_size is None:
            filtered_companies = [c for c in all_companies if c.get("team_size", 0) >= min_size]
            size_description = f"{min_size}+"
        else:
            filtered_companies = [c for c in all_companies if min_size <= c.get("team_size", 0) <= max_size]
            size_description = f"{min_size}-{max_size}"
                
        return {"size_range": size_description, "companies": filtered_companies}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)