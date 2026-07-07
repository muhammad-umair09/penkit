import os
import sys
from core.colors import Colors

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_box(title: str, lines: list):
    width = max(len(line) for line in lines) if lines else 40
    width = max(width, len(title)) + 4
    
    print(Colors.CYAN + "┌" + "─" * (width - 2) + "┐")
    print(Colors.CYAN + f"│ {Colors.WHITE}{title.ljust(width - 4)}{Colors.CYAN} │")
    print(Colors.CYAN + "├" + "─" * (width - 2) + "┤")
    for line in lines:
        print(Colors.CYAN + f"│ {Colors.YELLOW}{line.ljust(width - 4)}{Colors.CYAN} │")
    print(Colors.CYAN + "└" + "─" * (width - 2) + "┘")

def ask_report_export(module_name: str, target: str, data: dict):
    from core.report import ReportGenerator
    choice = input(f"\n{Colors.YELLOW}Export report? (y/n): ").strip().lower()
    if choice == 'y':
        fmt = input(f"{Colors.WHITE}Format (txt, json, csv, html, pdf) [json]: ").strip().lower()
        if not fmt:
            fmt = "json"
        rg = ReportGenerator()
        path = rg.export(module_name, target, data, fmt)
        print(Colors.success(f"Report cleanly compiled and dropped here: {path}"))