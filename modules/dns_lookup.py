import dns.resolver
from colorama import Fore, Style, init

init(autoreset=True)

def dns_lookup(domain):
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]

    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + "              PenKit DNS Lookup v1.0.0")
    print(Fore.CYAN + "=" * 60)
    print(f"{Fore.YELLOW}Target Domain: {Fore.WHITE}{domain}\n")

    for record in record_types:
        print(Fore.MAGENTA + f"[{record}] Records")

        try:
            answers = dns.resolver.resolve(domain, record)

            for answer in answers:
                print(Fore.GREEN + f"  • {answer}")

        except dns.resolver.NoAnswer:
            print(Fore.RED + "  No Record Found")

        except dns.resolver.NXDOMAIN:
            print(Fore.RED + "  Domain does not exist.")
            return
        except dns.resolver.Timeout:
            print("DNS request timed out")

        except Exception as e:
            print(Fore.RED + f"  Error: {e}")

        print()

    print(Fore.CYAN + "=" * 60)
    print(Fore.GREEN + "[+] DNS Lookup Completed Successfully")
    print(Fore.CYAN + "=" * 60)


if __name__ == "__main__":
    target = input("Enter Target Domain: ").strip()
    dns_lookup(target)

import dns.resolver

resolver = dns.resolver.Resolver()

resolver.nameservers = [
    "8.8.8.8",      # Google DNS
    "1.1.1.1"       # Cloudflare DNS
]

resolver.timeout = 5
resolver.lifetime = 10