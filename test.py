import requests

url = "https://yc-oss.github.io/api/companies/all.json"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for HTTP errors
    data = response.json()
    
    # Print the entire JSON response
    print(data)
    
    # Optionally, print a preview of the first few companies
    for company in data[:5]:
        print(f"Name: {company.get('name')}, URL: {company.get('url')}")
except requests.RequestException as e:
    print(f"API request failed: {e}")
