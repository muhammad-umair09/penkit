import whois
from core.colors import Colors

def run_whois(target: str) -> dict:
    print(Colors.info(f"Querying WHOIS registers for domain registry allocations: {target}"))
    results = {}
    try:
        w = whois.whois(target)
        results["Registrar"] = w.registrar
        results["Creation Date"] = str(w.creation_date)
        results["Expiry Date"] = str(w.expiration_date)
        results["Name Servers"] = w.name_servers
        results["Country"] = w.country
        print(Colors.success("Registry dataset populated correctly."))
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"WHOIS data lookup aborted: {e}"))
    return results