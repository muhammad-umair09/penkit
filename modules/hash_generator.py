import hashlib
import os
import requests
from core.colors import Colors

def identify_hash(hash_str: str) -> str:
    length = len(hash_str)
    if length == 32: return "MD5"
    elif length == 40: return "SHA-1"
    elif length == 64: return "SHA-256"
    elif length == 128: return "SHA-512"
    else: return "Unknown"

def online_lookup(target_hash: str, hash_type: str) -> str:
    """Internet API ke ziye lookup karne ke liye fallback functionality"""
    print(Colors.info(f"Querying online distributed signature databases for {hash_type}..."))
    try:
        # Giga-database signature verification channel API (Sample wrapper logic)
        # Note: Kuch APIs online token ya authentication maangti hain, yeh ek free public reverse tester hai
        url = f"https://api.hashify.net/hash/{hash_type.lower()}/{target_hash}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("Data"): # Agar plain text database mein mil gaya
                return data["Data"]
    except Exception:
        pass
    return None

def crack_hash(target_hash: str, hash_type: str, wordlist_path: str) -> bool:
    passwords = []
    
    if not wordlist_path:
        # Hamari local quick choti testing list
        passwords = [
            "admin", "password", "123456", "Admin123", "password@123", 
            "Umair@09", "Python@789", "root", "login"
        ]
    else:
        if not os.path.exists(wordlist_path):
            print(Colors.fail(f"Error: Wordlist file not found at '{wordlist_path}'"))
            return False
        try:
            with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(Colors.fail(f"Failed to read file: {e}"))
            return False

    print(Colors.info(f"Running local rapid comparison array..."))
    for word in passwords:
        if hash_type == "MD5": guess = hashlib.md5(word.encode()).hexdigest()
        elif hash_type == "SHA-1": guess = hashlib.sha1(word.encode()).hexdigest()
        elif hash_type == "SHA-256": guess = hashlib.sha256(word.encode()).hexdigest()
        elif hash_type == "SHA-512": guess = hashlib.sha512(word.encode()).hexdigest()
        else: return False
            
        if guess.lower() == target_hash.lower():
            print(f"\n{Colors.GREEN}[=== LOCAL RECOVERY SUCCESS ===]")
            print(f"  [+] Recovered Text  : {Colors.YELLOW}{word}\n")
            return True
            
    # --- UPGRADE FALLBACK: Agar local list mein nahi mila, to internet check karo ---
    print(Colors.info("Target not matched locally. Triggering advanced network translation..."))
    online_result = online_lookup(target_hash, hash_type)
    if online_result:
        print(f"\n{Colors.GREEN}[=== ONLINE CLOUD RECOVERY SUCCESS ===]")
        print(f"  [+] Source Identifier : API Cloud Database")
        print(f"  [+] Recovered Text    : {Colors.YELLOW}{online_result}\n")
        return True
        
    print(Colors.fail("\n[-] Exhaustion: Target signature not matched in local pool or online repositories."))
    return False

def generate_hashes(text: str) -> dict:
    print(f"\n{Colors.YELLOW}[1] Generate Hashes from Text")
    print(f"[2] Identify & Crack an existing Hash")
    sub_choice = input(f"{Colors.YELLOW}[?] Select Sub-Mode: ").strip()
    
    if sub_choice == "1":
        text = input("Enter payload data string to convert: ").strip()
        if not text: return {}
        results = {
            "MD5": hashlib.md5(text.encode()).hexdigest(),
            "SHA-1": hashlib.sha1(text.encode()).hexdigest(),
            "SHA-256": hashlib.sha256(text.encode()).hexdigest(),
            "SHA-512": hashlib.sha512(text.encode()).hexdigest()
        }
        print(f"\n{Colors.GREEN}[+] Cryptographic Generation Matrix Finished:")
        for alg, val in results.items():
            print(f"  [-] {alg.ljust(7)}: {val}")
        return results

    elif sub_choice == "2":
        target_hash = input("[?] Enter the target hash to analyze: ").strip().lower()
        if not target_hash: return {}
        hash_type = identify_hash(target_hash)
        print(Colors.info(f"Analyzing structure... Signature Match Found: {Colors.GREEN}{hash_type}"))
        if hash_type == "Unknown": return {}
            
        crack_choice = input(f"{Colors.YELLOW}[?] Do you want to attempt cracking? (y/n): ").strip().lower()
        if crack_choice == 'y':
            wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Auto-Cloud Lookup): ").strip()
            crack_hash(target_hash, hash_type, wordlist_path)
        return {"Target_Hash": target_hash, "Type": hash_type}