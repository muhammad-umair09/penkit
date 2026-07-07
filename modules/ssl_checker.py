import socket
import ssl
from datetime import datetime
from core.colors import Colors

def check_ssl_cert(hostname: str, port: int = 443) -> dict:
    print(Colors.info(f"Validating SSL/TLS Certificate configurations on {hostname}:{port}"))
    results = {}
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=4) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                subject = dict(x[0] for x in cert.get('subject', ()))
                issuer = dict(x[0] for x in cert.get('issuer', ()))
                
                results["Subject_CommonName"] = subject.get('commonName', 'Unknown')
                results["Issuer"] = issuer.get('commonName', 'Unknown')
                results["Valid_From"] = cert.get('notBefore')
                results["Expiry"] = cert.get('notAfter')
                
                # Expiry delta evaluation logic
                ts_format = r"%b %d %H:%M:%S %Y %Z"
                exp_dt = datetime.strptime(results["Expiry"], ts_format)
                remaining = exp_dt - datetime.utcnow()
                results["Days_Remaining"] = str(remaining.days)
                results["Cipher_Protocol"] = ssock.version()
                
                print(Colors.success(f"Valid TLS Context verified. Lifetime status: {results['Days_Remaining']} remaining days."))
    except Exception as e:
        results["Error"] = f"SSL Handshake context mismatch: {str(e)}"
        print(Colors.fail(f"SSL Validation processing aborted: {e}"))
    return results