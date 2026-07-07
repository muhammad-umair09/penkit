import os
from core.colors import Colors

def view_report_pipeline():
    """Workspace repositories se saved reports view karne ka main pipeline"""
    report_dir = "reports"
    
    print(f"\n{Colors.BLUE}[*] Isolated File Repositories inside local environment workspace:{Colors.RESET}")
    
    # Check agar reports ka folder exist nahi karta ya khali hai
    if not os.path.exists(report_dir) or not os.listdir(report_dir):
        print(Colors.fail("[-] No saved reports isolated in the workspace directory."))
        return
        
    # Sirf .txt files ko filter out karne ke liye
    files = [f for f in os.listdir(report_dir) if f.endswith('.txt')]
    if not files:
        print(Colors.fail("[-] No compatible report assets found."))
        return

    # FIXED: Yahan se Colors.white hata diya taaki crash na ho
    for idx, file_name in enumerate(files, 1):
        print(f"  [{idx}] {file_name}")

    try:
        choice = input(f"\n{Colors.YELLOW}[?] Enter report number to read (or press Enter to cancel): ").strip()
        if not choice:
            return

        file_idx = int(choice) - 1
        if 0 <= file_idx < len(files):
            target_file = os.path.join(report_dir, files[file_idx])
            
            print(f"\n{Colors.GREEN}[=== READING REPORT: {files[file_idx]} ===]{Colors.RESET}\n")
            
            # File read karke print karne ka loop
            with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    print(line.rstrip())
                    
            print(f"\n{Colors.GREEN}[=== END OF REPORT EXECUTION DUMP ===]{Colors.RESET}\n")
        else:
            print(Colors.fail("Error: Selection out of bounds inside active repository array."))
            
    except ValueError:
        print(Colors.fail("Error: Invalid numeric formatting configuration input."))
    except Exception as e:
        print(Colors.fail(f"Execution handling failure: {e}"))