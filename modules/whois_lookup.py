import whois

def run_whois(domain):
    try:
        data = whois.query(domain)

        if data is None:
            print("No WHOIS information found.")
            return

        print("Domain:", data.name)
        print("Registrar:", data.registrar)
        print("Creation:", data.creation_date)
        print("Expiry:", data.expiration_date)
        print("Name Servers:", data.name_servers)

    except Exception as e:
        print(f"Error: {e}")