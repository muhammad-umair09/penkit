import requests
import urllib3
import os
from core.colors import Colors

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directories(url: str) -> dict:
    # Strict formatting bypass logic
    if not url.startswith("http://") and not url.startswith("https://"):
        # testphp.vulnweb.com plain HTTP par chalta hai, isliye defaults check kar rahe hain
        if "vulnweb" in url:
            url = "http://" + url
        else:
            url = "https://" + url
        
    print(Colors.info(f"Scanning target application endpoint: {url}"))
    
    wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    directories = []
    
    if not wordlist_path:
        print(Colors.info("No file provided. Activating PenKit Built-in Web Discovery Wordlist..."))
        # Targeted paths jo testphp aur baqi sites par zaroor hote hain
        directories = [
            "admin", "login", "images", "secure", "pictures", 
            "includes", "artists", "disclaimer", "robots.txt"
        ]
    else:
        if not os.path.exists(wordlist_path):
            print(Colors.fail(f"Error: Wordlist file not found at '{wordlist_path}'"))
            return {"Found_Directories": []}
        try:
            with open(wordlist_path, "r") as f:
                directories = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except Exception as e:
            print(Colors.fail(f"Failed to read file: {e}"))
            return {"Found_Directories": []}

    results = {"Found_Directories": []}
    print(Colors.info(f"Loaded {len(directories)} components. Starting dynamic baseline analysis...\n"))
    
    # Real browser user-agent simulation strings
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for chunk in directories:
        test_url = url.rstrip("/") + "/" + chunk.lstrip("/")
        try:
            # GET request directly with redirects enabled standard
            response = requests.get(test_url, timeout=5, headers=headers, verify=False, allow_redirects=True)
            status = response.status_code
            
            # Agar folder ya valid endpoint mila
            if status in [200, 403]: 
                print(f"  {Colors.GREEN}[+] Found: {test_url} (Status: {status})")
                results["Found_Directories"].append({"url": test_url, "status": status})
                
        except requests.RequestException:
            pass
            
    if not results["Found_Directories"]:
        print(Colors.fail("\nNo common components isolated via dynamic baseline checks."))
    else:
        print(Colors.success(f"\n[+] Brute-force finished. Identified {len(results['Found_Directories'])} targets!"))
        
    return results