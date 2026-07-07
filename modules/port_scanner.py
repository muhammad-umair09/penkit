import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from core.colors import Colors
from core.logger import logger
from core.progress import draw_progress_bar

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 
    445: "SMB", 1433: "MSSQL", 3306: "MySQL", 3389: "RDP"
}

def scan_single_port(target_ip: str, port: int, timeout: float) -> dict:
    res = {"port": port, "status": "closed", "service": "unknown", "banner": ""}
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            res["status"] = "open"
            res["service"] = COMMON_PORTS.get(port, "unknown")
            try:
                s.send(b"Hello\r\n")
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                res["banner"] = banner.replace("\n", " ")
            except Exception:
                pass
        s.close()
    except Exception:
        pass
    return res

def run_port_scanner(target: str, port_mode: str, custom_ports: list = None, threads: int = 10, timeout: float = 2.0) -> dict:
    print(Colors.info(f"Resolving network target: {target}"))
    try:
        target_ip = socket.gethostbyname(target)
    except Exception as e:
        print(Colors.fail(f"Host resolution failed: {e}"))
        return {}

    ports_to_scan = []
    if port_mode == "common":
        ports_to_scan = list(COMMON_PORTS.keys())
    elif port_mode == "custom" and custom_ports:
        ports_to_scan = custom_ports
        
    print(Colors.info(f"Scanning target {target_ip} across {len(ports_to_scan)} targets..."))
    logger.info(f"Port scan started for {target_ip}")
    
    results = {}
    completed = 0
    total = len(ports_to_scan)
    
    if total == 0:
        print(Colors.warn("No structural targets provided to parse."))
        return {}

    draw_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=30)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_single_port, target_ip, port, timeout): port for port in ports_to_scan}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            draw_progress_bar(completed, total, prefix='Progress:', suffix='Complete', length=30)
            if res["status"] == "open":
                results[f"Port {res['port']}"] = f"OPEN | Service: {res['service']} | Banner: {res['banner']}"
                print(f"\n{Colors.GREEN}[+] Found Open Port: {res['port']} ({res['service']})")

    return results