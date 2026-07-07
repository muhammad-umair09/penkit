import requests
from core.colors import Colors

def parse_robots_txt(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    parsed_url = url.split("//")[-1].split("/")[0]
    target_robots = f"https://{parsed_url}/robots.txt"
    
    print(Colors.info(f"Targeting infrastructure discovery component: {target_robots}"))
    results = {"Target": target_robots, "Status": "Not Found", "Disallowed_Paths_Count": 0}
    
    try:
        res = requests.get(target_robots, timeout=5, verify=False)
        if res.status_code == 200:
            results["Status"] = "Found"
            lines = res.text.split("\n")
            disallowed = [line.strip() for line in lines if line.lower().startswith("disallow:")]
            results["Disallowed_Paths_Count"] = len(disallowed)
            results["Sample_Disallowed"] = ", ".join(disallowed[:5]) if disallowed else "None"
            print(Colors.success(f"robots.txt found. Isolated paths identified: {len(disallowed)}"))
        else:
            print(Colors.warn(f"Asset dropped with code status response: {res.status_code}"))
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"Connection aborted during endpoint collection parsing: {e}"))
    return results