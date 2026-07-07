import os
from core.colors import Colors

def display_banner():
    banner_path = "assets/banner.txt"
    logo_path = "assets/logo.txt"
    
    print(Colors.GREEN)
    if os.path.exists(banner_path):
        with open(banner_path, "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("=== PenKit Penetration Testing Toolkit ===")
        
    print(Colors.CYAN)
    if os.path.exists(logo_path):
        with open(logo_path, "r", encoding="utf-8") as f:
            print(f.read())
            
    print(Colors.WHITE + " Version: 1.0.0 | Operational Context: Authorized Labs & Audits Only")
    print(Colors.YELLOW + " Disclaimer: Illegal execution against unapproved assets is prohibited.")
    print(Colors.GREEN + "=" * 74 + "\n")