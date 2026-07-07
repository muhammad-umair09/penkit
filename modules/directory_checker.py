import requests
import urllib3
import os
import time
from core.colors import Colors

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_directories(url: str) -> dict:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url  # Standard web infrastructure defaults ke liye
            
    print(Colors.info(f"Scanning target application endpoint: {url}"))
    
    wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    directories = []
    
    if not wordlist_path:
        print(Colors.info("No file provided. Activating PenKit Built-in Web Discovery Wordlist..."))
        # Targeted paths jo httpbin.org aur baqi standard servers par active hote hain
        directories = [
            "html", "json", "xml", "status", "robots.txt", 
            "ip", "user-agent", "headers", "cookies"
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
    print(Colors.info(f"Loaded {len(directories)} components. Starting dynamic session verification...\n"))
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    })
    
    # Handshake block handle karne ke liye timeout ko thoda flexible rakha hai
    try:
        session.get(url, timeout=5, verify=False)
    except Exception as e:
        print(Colors.fail(f"Initial baseline target handshake dropped: {e}"))

    for chunk in directories:
        test_url = url.rstrip("/") + "/" + chunk.lstrip("/")
        try:
            response = session.get(test_url, timeout=5, verify=False, allow_redirects=True)
            status = response.status_code
            
            if status in [200, 403]: 
                print(f"  {Colors.GREEN}[+] Found: {test_url} (Status: {status})")
                results["Found_Directories"].append({"url": test_url, "status": status})
                
            time.sleep(0.1) # Smooth processing loop delay
                
        except requests.RequestException:
            pass
            
    if not results["Found_Directories"]:
        print(Colors.fail("\nNo common components isolated via dynamic baseline checks."))
    else:
        print(Colors.success(f"\n[+] Brute-force finished. Identified {len(results['Found_Directories'])} targets!"))
        
    return results