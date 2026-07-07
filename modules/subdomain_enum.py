import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.colors import Colors

COMMON_SUBDOMAINS = ["www", "mail", "ftp", "admin", "blog", "cpanel", "whm", "webmail", "webdisk", "dev", "staging", "api", "vpn"]

def check_subdomain(sub: str, domain: str) -> tuple:
    target = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(target)
        return target, ip
    except Exception:
        return target, None

def enumerate_subdomains(domain: str, threads: int = 10) -> dict:
    print(Colors.info(f"Executing dictionary subdomain validation checks for: {domain}"))
    results = {}
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_subdomain, sub, domain) for sub in COMMON_SUBDOMAINS]
        for future in as_completed(futures):
            target, ip = future.result()
            if ip:
                results[target] = ip
                print(Colors.success(f"Located active record: {target} -> {ip}"))
                
    if not results:
        print(Colors.warn("No standard workspace components resolved via dictionary map."))
    return results