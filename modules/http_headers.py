import requests
from core.colors import Colors

def analyze_http_headers(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(Colors.info(f"Connecting to live API/Web server engine asset: {url}"))
    results = {}
    try:
        response = requests.get(url, timeout=5, verify=False)
        hdrs = response.headers
        results["Server"] = hdrs.get("Server", "Not Disclosed")
        results["Powered-By"] = hdrs.get("X-Powered-By", "Not Disclosed")
        results["Content-Type"] = hdrs.get("Content-Type", "Not Disclosed")
        results["Cache-Control"] = hdrs.get("Cache-Control", "Not Configured")
        results["Set-Cookie"] = "Present" if "Set-Cookie" in hdrs else "Absent"
        
        for k, v in results.items():
            print(Colors.white(f"  {k}: {v}"))
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Server response extraction disrupted: {e}"))
    return results