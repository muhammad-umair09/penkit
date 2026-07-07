import os
from datetime import datetime
from core.colors import Colors

class ReportGenerator:
    """Network scanning aur baki modules ki reports save karne ke liye"""
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def write_report(self, content: str) -> str:
        """Data ko text file mein formatting ke sath write karne ke liye"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.module_name}_{timestamp}.txt"
        filepath = os.path.join(self.report_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"=== PenKit Security Assessment Report ===\n")
                f.write(f"Module    : {self.module_name.upper()}\n")
                f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n\n")
                f.write(content)
            return filepath
        except Exception as e:
            print(Colors.fail(f"Failed to generate report file: {e}"))
            return ""

def view_report_pipeline():
    """Workspace repositories se saved reports view karne ka pipeline (Option 14)"""
    report_dir = "reports"
    
    print(f"\n{Colors.BLUE}[*] Isolated File Repositories inside local environment workspace:{Colors.RESET}")
    
    if not os.path.exists(report_dir) or not os.listdir(report_dir):
        print(Colors.fail("[-] No saved reports isolated in the workspace directory."))
        return
        
    files = [f for f in os.listdir(report_dir) if f.endswith('.txt')]
    if not files:
        print(Colors.fail("[-] No compatible report assets found."))
        return

    # Safe layout printing loop without 'Colors.white' attribute
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