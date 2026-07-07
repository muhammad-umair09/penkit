import whois

def run_whois(domain):
    try:
        data = whois.whois(domain)

        print("Domain:", data.domain_name)
        print("Registrar:", data.registrar)
        print("Creation:", data.creation_date)
        print("Expiry:", data.expiration_date)

    except Exception as e:
        print(f"Error: {e}")