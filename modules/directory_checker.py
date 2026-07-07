import requests
from core.colors import Colors

COMMON_DIR_LIST = ["admin", "login", "config", "backup", "api", "secret", "db", "uploads"]

def check_directories(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    base_url = url.rstrip("/")
    print(Colors.info(f"Scanning target application endpoint against structural layouts: {base_url}"))
    results = {}
    
    for directory in COMMON_DIR_LIST:
        target_endpoint = f"{base_url}/{directory}"
        try:
            res = requests.head(target_endpoint, timeout=3, verify=False)
            if res.status_code in [200, 301, 302, 403]:
                results[f"/{directory}"] = f"Status Code: {res.status_code}"
                print(Colors.success(f" Identified deployment structural component: /{directory} ({res.status_code})"))
        except Exception:
            pass
            
    if not results:
        print(Colors.info("No common components isolated via rapid head checks."))
    return results