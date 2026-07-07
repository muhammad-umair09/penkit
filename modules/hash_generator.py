import hashlib
import os
import requests
from core.colors import Colors

def identify_hash(hash_str: str) -> str:
    # UPGRADE: Bcrypt structural signature patterns detection
    if hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        return "bcrypt"
        
    length = len(hash_str)
    if length == 32: return "MD5"
    elif length == 40: return "SHA-1"
    elif length == 64: return "SHA-256"
    elif length == 128: return "SHA-512"
    else: return "Unknown"

def online_lookup(target_hash: str, hash_type: str) -> str:
    print(Colors.info(f"Querying online distributed signature databases for {hash_type}..."))
    try:
        # standard fallback web cloud channels
        url = f"https://api.hashify.net/hash/{hash_type.lower()}/{target_hash}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("Data"):
                return data["Data"]
    except Exception:
        pass
    return None

def crack_hash(target_hash: str, hash_type: str, wordlist_path: str) -> bool:
    # Bcrypt slow performance warning parameter representation
    if hash_type == "bcrypt":
        print(Colors.YELLOW + "\n[!] Warning: bcrypt utilizes high key-stretching costs.")
        print("[!] Local brute force might be significantly slower without GPU arrays." + Colors.RESET)
        
    passwords = []
    if not wordlist_path:
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

    print(Colors.info(f"Running cryptographic comparison array against target..."))
    
    # Standard algorithms mapping
    for word in passwords:
        guess = ""
        if hash_type == "MD5": guess = hashlib.md5(word.encode()).hexdigest()
        elif hash_type == "SHA-1": guess = hashlib.sha1(word.encode()).hexdigest()
        elif hash_type == "SHA-256": guess = hashlib.sha256(word.encode()).hexdigest()
        elif hash_type == "SHA-512": guess = hashlib.sha512(word.encode()).hexdigest()
        elif hash_type == "bcrypt":
            # Note: Bcrypt uses unique salt parameters per generation.
            # Real decryption checks require specialized library modules like 'bcrypt'.
            # For this pipeline, we fall through to cloud resolution to guarantee instantaneous speed.
            break
            
        if guess and guess.lower() == target_hash.lower():
            print(f"\n{Colors.GREEN}[=== LOCAL RECOVERY SUCCESS ===]")
            print(f"  [+] Recovered Text  : {Colors.YELLOW}{word}\n")
            return True
            
    # Cloud check bypass routing trigger
    print(Colors.info("Target signature mismatch locally. Initiating cloud-database reverse matching..."))
    online_result = online_lookup(target_hash, hash_type)
    if online_result:
        print(f"\n{Colors.GREEN}[=== ONLINE CLOUD RECOVERY SUCCESS ===]")
        print(f"  [+] Source Identifier : Cloud API Matrix Target")
        print(f"  [+] Recovered Text    : {Colors.YELLOW}{online_result}\n")
        return True
        
    print(Colors.fail("\n[-] Exhaustion: Target string signature could not be extracted."))
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
        target_hash = input("[?] Enter the target hash to analyze: ").strip()
        if not target_hash: return {}
        
        hash_type = identify_hash(target_hash)
        print(Colors.info(f"Analyzing structure... Signature Match Found: {Colors.GREEN}{hash_type}"))
        
        if hash_type == "Unknown":
            print(Colors.fail("Unsupported or un-identifiable hash format structure length."))
            return {}
            
        crack_choice = input(f"{Colors.YELLOW}[?] Do you want to attempt cracking? (y/n): ").strip().lower()
        if crack_choice == 'y':
            wordlist_path = input(f"{Colors.YELLOW}[?] Enter Wordlist Path (or press Enter for Auto-Cloud Lookup): ").strip()
            crack_hash(target_hash, hash_type, wordlist_path)
        return {"Target_Hash": target_hash, "Type": hash_type}