import socket
from core.colors import Colors

def grab_banner(target: str, port: int, timeout: float = 3.0) -> dict:
    print(Colors.info(f"Attempting volatile banner extraction from {target}:{port}"))
    results = {"Target": target, "Port": port, "Banner": "Failed to collect"}
    try:
        ip = socket.gethostbyname(target)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # Payload trigger variant matching standard protocol conventions
        s.sendall(b"HEAD / HTTP/1.1\r\nHost: " + target.encode() + b"\r\n\r\n")
        raw = s.recv(1024)
        banner = raw.decode('utf-8', errors='ignore').strip()
        if banner:
            results["Banner"] = banner.replace("\r", "").replace("\n", " | ")
            print(Colors.success(f"Banner identified: {results['Banner'][:60]}..."))
        s.close()
    except Exception as e:
        results["Banner"] = f"Extraction context error: {str(e)}"
        print(Colors.fail(f"Banner collection dropped: {e}"))
    return results