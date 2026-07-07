import dns.resolver
from core.colors import Colors

def dns_query(target: str) -> dict:
    print(Colors.info(f"Running full zone infrastructure mapping for: {target}"))
    records = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]
    results = {}
    
    for rec in records:
        try:
            answers = dns.resolver.resolve(target, rec)
            results[rec] = [str(rdata) for rdata in answers]
            print(Colors.success(f"Mapped {rec} record successfully."))
        except Exception:
            results[rec] = ["None or Resolution Error"]
            
    return results