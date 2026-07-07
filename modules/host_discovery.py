import socket
import subprocess
import platform
import time
from core.colors import Colors
from core.logger import logger

def discover_host(target: str) -> dict:
    print(Colors.info(f"Initiating discovery suite against target: {target}"))
    logger.info(f"Host discovery initiated for target: {target}")
    
    results = {"Target": target, "Status": "Unknown", "Latency": "N/A", "Resolved_IP": "N/A"}
    
    try:
        ip = socket.gethostbyname(target)
        results["Resolved_IP"] = ip
    except Exception as e:
        results["Status"] = "Resolution Failed"
        print(Colors.fail(f"Could not resolve host: {e}"))
        return results

    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "2", ip]
    
    start_time = time.time()
    try:
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=4)
        latency = f"{(time.time() - start_time) * 1000 / 2:.2f}ms"
        if proc.returncode == 0:
            results["Status"] = "Active"
            results["Latency"] = latency
            print(Colors.success(f"Host online. Metric Latency: {latency}"))
        else:
            # Fallback to connection test
            results = _fallback_discovery(ip, results)
    except Exception:
        results = _fallback_discovery(ip, results)
        
    return results

def _fallback_discovery(ip: str, results: dict) -> dict:
    print(Colors.warn("Ping blocked or failed. Executing TCP fallback discovery probe..."))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        res = s.connect_ex((ip, 80))
        if res == 0:
            results["Status"] = "Active (Via TCP/80)"
            print(Colors.success("Target alive via Web Service connection handshake."))
        else:
            results["Status"] = "Unresponsive / Filtered"
            print(Colors.fail("Host did not respond to standard ICMP or TCP probes."))
        s.close()
    except Exception as e:
        results["Status"] = f"Error: {str(e)}"
    return results