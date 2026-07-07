import hashlib
from core.colors import Colors

def generate_hashes(data_string: str) -> dict:
    print(Colors.info("Computing cryptographic digests across multi-algorithm arrays..."))
    b_data = data_string.encode('utf-8')
    
    results = {
        "Input String": data_string,
        "MD5": hashlib.md5(b_data).hexdigest(),
        "SHA1": hashlib.sha1(b_data).hexdigest(),
        "SHA256": hashlib.sha256(b_data).hexdigest(),
        "SHA512": hashlib.sha512(b_data).hexdigest()
    }
    
    for k, v in results.items():
        if k != "Input String":
            print(Colors.white(f"  {k}: {v}"))
            
    return results