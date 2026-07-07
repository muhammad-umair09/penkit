import sys
import os

# Add root folder to module search vector paths to fix execution reference contexts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.colors import Colors
from core.banner import display_banner
from core.progress import animated_loading
from core.helpers import clear_screen, print_box, ask_report_export
from core.config_loader import load_config
from core.validator import Validator

# Module Function Imports
from modules.host_discovery import discover_host
from modules.port_scanner import run_port_scanner
from modules.banner_grabber import grab_banner
from modules.dns_lookup import dns_query
from modules.whois_lookup import run_whois
from modules.subdomain_enum import enumerate_subdomains
from modules.http_headers import analyze_http_headers
from modules.ssl_checker import check_ssl_cert
from modules.security_headers import analyze_security_headers
from modules.robots_parser import parse_robots_txt
from modules.directory_checker import check_directories
from modules.hash_generator import generate_hashes
from modules.base64_tool import process_base64

def display_menu():
    print(Colors.CYAN + "┌" + "─" * 45 + "┐")
    print(Colors.CYAN + "│" + Colors.WHITE + "      PENKIT OPERATIONAL COMMAND SYSTEM      " + Colors.CYAN + "│")
    print(Colors.CYAN + "├" + "─" * 45 + "┤")
    menu_options = [
        "1. Host Discovery", "2. Port Scanner", "3. Banner Grabber",
        "4. DNS Lookup", "5. WHOIS Lookup", "6. Subdomain Enumeration",
        "7. HTTP Header Analyzer", "8. SSL Certificate Checker", "9. Security Headers Checker",
        "10. Robots.txt Parser", "11. Directory Checker", "12. Hash Generator",
        "13. Base64 Encoder/Decoder", "14. View Saved Reports", "15. Settings",
        "16. Help", "17. About", "0. Exit Execution Pipeline"
    ]
    for opt in menu_options:
        print(Colors.CYAN + f"│ {Colors.YELLOW}{opt.ljust(43)}{Colors.CYAN} │")
    print(Colors.CYAN + "└" + "─" * 45 + "┘")

def view_saved_reports(folder: str):
    if not os.path.exists(folder) or not os.listdir(folder):
        print(Colors.warn("No compiled testing logs discovered inside working scope storage."))
        return
    print(Colors.info("Isolated File Repositories inside local environment workspace:"))
    for f in os.listdir(folder):
        print(Colors.white(f" - {f}"))

def display_help():
    lines = [
        "1-3: Map active machines and parse open interfaces.",
        "4-6: Interrogate registry and DNS domain routing.",
        "7-11: Analyze security settings of web targets.",
        "12-13: Structural mathematical format pipelines."
    ]
    print_box("Help Matrix & Operational Scope", lines)

def display_about():
    lines = [
        "Name: PenKit Core Utility",
        "Context: Defense Auditing & Lab Simulation Tools",
        "License: Open Source MIT Infrastructure Blueprint"
    ]
    print_box("Core Architecture Data", lines)

def main():
    clear_screen()
    animated_loading(1.0)
    config = load_config()
    timeout = config["settings"]["timeout"]
    threads = config["settings"]["threads"]
    report_dir = config["settings"]["output_folder"]

    while True:
        clear_screen()
        display_banner()
        display_menu()
        
        try:
            choice = input(f"\n{Colors.GREEN}PenKit >> {Colors.WHITE}").strip()
            if choice == "0":
                print(Colors.info("Terminating environment control system context loop cleanly."))
                break
            elif choice == "1":
                target = input("Enter target host/IP: ").strip()
                if target:
                    res = discover_host(target)
                    ask_report_export("host_discovery", target, res)
            elif choice == "2":
                target = input("Enter target host/IP: ").strip()
                mode = input("Scan mode (common/custom): ").strip().lower()
                custom_ports = []
                if mode == "custom":
                    p_str = input("Enter target ports comma-separated (e.g. 22,80,443): ").strip()
                    custom_ports = [int(p) for p in p_str.split(",") if p.strip().isdigit()]
                res = run_port_scanner(target, mode, custom_ports, threads, timeout)
                ask_report_export("port_scan", target, res)
            elif choice == "3":
                target = input("Enter target host/IP: ").strip()
                port = int(input("Enter target port: ").strip())
                res = grab_banner(target, port, timeout)
                ask_report_export("banner_grab", target, res)
            elif choice == "4":
                target = input("Enter target domain: ").strip()
                if Validator.is_valid_domain(target):
                    res = dns_query(target)
                    ask_report_export("dns_lookup", target, res)
                else:
                    print(Colors.fail("Domain validation dropped input structure."))
            elif choice == "5":
                target = input("Enter domain: ").strip()
                res = run_whois(target)
                ask_report_export("whois", target, res)
            elif choice == "6":
                target = input("Enter parent domain: ").strip()
                res = enumerate_subdomains(target, threads)
                ask_report_export("subdomains", target, res)
            elif choice == "7":
                target = input("Enter URL/Host: ").strip()
                res = analyze_http_headers(target)
                ask_report_export("http_headers", target, res)
            elif choice == "8":
                target = input("Enter Host domain: ").strip()
                res = check_ssl_cert(target)
                ask_report_export("ssl_cert", target, res)
            elif choice == "9":
                target = input("Enter web app target link: ").strip()
                res = analyze_security_headers(target)
                ask_report_export("security_headers", target, res)
            elif choice == "10":
                target = input("Enter target host domain: ").strip()
                res = parse_robots_txt(target)
                ask_report_export("robots_txt", target, res)
            elif choice == "11":
                target = input("Enter target application base URL: ").strip()
                res = check_directories(target)
                ask_report_export("directory_check", target, res)
            elif choice == "12":
                target = input("Enter payload data string to convert: ").strip()
                res = generate_hashes(target)
                ask_report_export("hashes", "local_data", res)
            elif choice == "13":
                target = input("Enter processing string element: ").strip()
                mode = input("Transform type action (encode/decode): ").strip().lower()
                res = process_base64(target, mode)
                ask_report_export("base64", "transformed_element", res)
            elif choice == "14":
                view_saved_reports(report_dir)
            elif choice == "15":
                print(Colors.info(f"Loaded Contexts: Timeout: {timeout}s | Execution Vector Capacity: {threads} threads"))
            elif choice == "16":
                display_help()
            elif choice == "17":
                display_about()
            else:
                print(Colors.fail("Unrecognized input format parameter selection."))
                
            input(f"\n{Colors.CYAN}Press Enter to return to main terminal interface context...")
        except KeyboardInterrupt:
            print(f"\n{Colors.warn('SigKill interrupt detected. Forcing cleanly structured termination...')}")
            sys.exit(0)
        except Exception as e:
            print(Colors.fail(f"Execution handling failure: {e}"))
            input("\nPress Enter to restart console pipeline...")

if __name__ == "__main__":
    main()