import requests
from core.colors import Colors

SEC_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-Content-Type-Options"
]

def analyze_security_headers(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    print(Colors.info(f"Analyzing Defensive Hardening Headers for: {url}"))
    results = {}
    try:
        res = requests.get(url, timeout=5, verify=False)
        for header in SEC_HEADERS:
            status = res.headers.get(header)
            if status:
                results[header] = f"Configured: {status[:40]}"
                print(Colors.success(f" Found: {header}"))
            else:
                results[header] = "Missing / Not Enforced"
                print(Colors.fail(f" Missing: {header}"))
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Could not connect to evaluate runtime hardening state: {e}"))
    return results