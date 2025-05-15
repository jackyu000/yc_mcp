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

if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)