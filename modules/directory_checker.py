import requests
from core.colors import Colors
from core.report import ReportGenerator

def check_directories() -> dict:
    print(f"\n{Colors.YELLOW}[=== Directory Checker Suite ===]")
    target_url = input("Enter target application base URL (e.g. http://example.com): ").strip()
    
    # Input Validation
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url

    wordlist_choice = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Built-in list): ").strip()
    
    # Quick Built-in list fallback
    if not wordlist_choice:
        print(Colors.info("Activating PenKit Built-in Web Discovery Wordlist..."))
        directories = ["admin", "login", "config.php", "db", "uploads", "robots.txt", "dashboard"]
    else:
        try:
            with open(wordlist_choice, "r") as f:
                directories = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(Colors.fail(f"Failed to read custom wordlist: {e}"))
            return {}

    found_assets = {}
    print(Colors.info("Starting baseline network target handshake verification..."))
    
    # CRITICAL FIX: Graceful handling of connection exceptions & timeouts
    try:
        base_test = requests.get(target_url, timeout=5)
        print(Colors.info(f"Target system alive. Main stream responding with HTTP {base_test.status_code}"))
    except requests.exceptions.Timeout:
        print(Colors.fail("[-] Baseline target handshake dropped: Connection timeout reached (Server too slow)."))
        return {}
    except requests.exceptions.ConnectionError:
        print(Colors.fail("[-] Baseline target handshake dropped: Connection reset or invalid hostname lookup resolved."))
        return {}
    except Exception as e:
        print(Colors.fail(f"[-] Connectivity matrix mapping fault: {e}"))
        return {}

    # Sequential directory analysis
    for folder in directories:
        url = f"{target_url.rstrip('/')}/{folder}"
        try:
            res = requests.get(url, timeout=3, allow_redirects=False)
            if res.status_code == 200:
                print(f"  {Colors.GREEN}[+] Found Asset : {url} (Status: 200 OK){Colors.RESET}")
                found_assets[folder] = "200 OK"
            elif res.status_code in [301, 302]:
                print(f"  {Colors.YELLOW}[!] Redirect    : {url} -> {res.headers.get('Location')}{Colors.RESET}")
                found_assets[folder] = f"Redirect ({res.status_code})"
        except requests.exceptions.RequestException:
            continue # Skip individual timeouts silently to maintain stream integrity

    if not found_assets:
        print(Colors.fail("\n[-] No common components isolated via dynamic baseline checks."))
    else:
        export_choice = input(f"\n{Colors.YELLOW}[?] Export report? (y/n): ").strip().lower()
        if export_choice == 'y':
            fmt = input("Format (txt, json, csv, html) [txt]: ").strip().lower() or "txt"
            reporter = ReportGenerator("directory_scanner")
            saved_path = reporter.write_report(found_assets, fmt)
            print(f"{Colors.GREEN}[+] Audit logs generated at: {saved_path}")

    return found_assets