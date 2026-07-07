import socket
import ssl
from datetime import datetime
from core.colors import Colors

def check_ssl_cert(hostname: str, port: int = 443) -> dict:
    print(Colors.info(f"Initiating Advanced Deep SSL/TLS Audit on {hostname}:{port}"))
    results = {
        "Target": f"{hostname}:{port}",
        "Protocols_Supported": [],
        "Vulnerabilities": []
    }
    
    # Standard security map
    test_versions = {
        "SSLv3": ssl.TLSVersion.SSLv3 if hasattr(ssl.TLSVersion, 'SSLv3') else None,
        "TLSv1.0": ssl.TLSVersion.TLSv1 if hasattr(ssl.TLSVersion, 'TLSv1') else None,
        "TLSv1.1": ssl.TLSVersion.TLSv1_1 if hasattr(ssl.TLSVersion, 'TLSv1_1') else None,
        "TLSv1.2": ssl.TLSVersion.TLSv1_2 if hasattr(ssl.TLSVersion, 'TLSv1_2') else None,
        "TLSv1.3": ssl.TLSVersion.TLSv1_3 if hasattr(ssl.TLSVersion, 'TLSv1_3') else None
    }
    
    # Individual precise handshake loop
    for name, version_enum in test_versions.items():
        if version_enum is None:
            continue
        try:
            # TLS_CLIENT mode automatically configures verification parameters safely
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            context.minimum_version = version_enum
            context.maximum_version = version_enum
            
            with socket.create_connection((hostname, port), timeout=3) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    # Connection successfully bounded strictly to target type
                    results["Protocols_Supported"].append(name)
        except Exception:
            # If handshake drops, target does not support this exact configuration
            pass

    # Global connection layer for metadata parsing
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                active_ver = ssock.version()
                
                # Check mapping for dynamic outputs fallback logic
                clean_ver = active_ver.replace("TLSv", "TLSv1.") if active_ver == "TLSv1" else active_ver
                if clean_ver not in results["Protocols_Supported"]:
                    results["Protocols_Supported"].append(clean_ver)
                
                subject = dict(x[0] for x in cert.get('subject', ()))
                issuer = dict(x[0] for x in cert.get('issuer', ()))
                
                results["Subject_CN"] = subject.get('commonName', 'Unknown')
                results["Issuer_CN"] = issuer.get('commonName', 'Unknown')
                results["Expiry"] = cert.get('notAfter')
                
                ts_format = r"%b %d %H:%M:%S %Y %Z"
                exp_dt = datetime.strptime(results["Expiry"], ts_format)
                remaining = exp_dt - datetime.utcnow()
                results["Days_Remaining"] = remaining.days
                
                # Dynamic Security Evaluation Engine
                insecure_found = [p for p in ["SSLv3", "TLSv1.0", "TLSv1.1"] if p in results["Protocols_Supported"]]
                if insecure_found:
                    results["Vulnerabilities"].append(f"Accepts Deprecated Protocols ({', '.join(insecure_found)})")
                
                if remaining.days <= 0:
                    results["Vulnerabilities"].append("Certificate EXPIRED")
                
                # Clean screen outputs presentation mapping
                print(f"\n{Colors.GREEN}[+] SSL Audit Completed Successfully!")
                print(f"  {Colors.WHITE}Issuer: {results['Issuer_CN']}")
                print(f"  {Colors.WHITE}Days Remaining: {results['Days_Remaining']}")
                
                # Clean duplicate and format sorting string errors
                final_protocols = sorted(list(set(results["Protocols_Supported"])))
                print(f"  {Colors.WHITE}Supported Protocols: {final_protocols}")
                
                if results["Vulnerabilities"]:
                    print(f"  {Colors.RED}Vulnerabilities Detected: {results['Vulnerabilities']}")
                else:
                    print(f"  {Colors.GREEN}Vulnerabilities Detected: None (Secure Setup)")
                    
    except Exception as e:
        results["Error"] = str(e)
        print(Colors.fail(f"SSL Handshake/Audit aborted: {e}"))
        
    return results