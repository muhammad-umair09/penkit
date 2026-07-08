import os
import json
import csv
from datetime import datetime
from core.colors import Colors

class ReportGenerator:
    """Advanced Multi-Format Professional Reporting System"""
    def __init__(self, module_name: str):
        self.module_name = module_name or "general_module"
        self.report_dir = "reports"
        if not os.path.exists(self.report_dir):
            os.makedirs(self.report_dir)

    def write_report(self, content_data, export_format: str = "txt") -> str:
        """Saves reports into requested professional formats securely"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.module_name}_{timestamp}.{export_format.lower()}"
        filepath = os.path.join(self.report_dir, filename)
        
        try:
            # === TXT FORMAT ===
            if export_format.lower() == "txt":
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"=== PenKit Security Assessment Report ===\n")
                    f.write(f"Module    : {self.module_name.upper()}\n")
                    f.write(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(str(content_data))
            
            # === JSON FORMAT ===
            elif export_format.lower() == "json":
                with open(filepath, "w", encoding="utf-8") as f:
                    report_struct = {
                        "tool": "PenKit",
                        "module": self.module_name,
                        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "data": content_data
                    }
                    json.dump(report_struct, f, indent=4)
            
            # === CSV FORMAT ===
            elif export_format.lower() == "csv":
                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Metadata_Key", "Metadata_Value"])
                    writer.writerow(["Module", self.module_name])
                    writer.writerow(["Timestamp", datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    if isinstance(content_data, dict):
                        for k, v in content_data.items():
                            writer.writerow([k, v])
                    else:
                        writer.writerow(["Raw Output Data", str(content_data)])

            # === HTML FORMAT ===
            elif export_format.lower() == "html":
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"<html><head><title>PenKit Report - {self.module_name}</title>")
                    f.write("<style>body{font-family:Arial;background:#1e1e1e;color:#fff;padding:20px;}")
                    f.write("h1{color:#00ff00;} pre{background:#2d2d2d;padding:15px;border-radius:5px;}</style></head><body>")
                    f.write(f"<h1>PenKit Audit: {self.module_name.upper()}</h1>")
                    f.write(f"<p><b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p><hr>")
                    f.write(f"<pre>{str(content_data)}</pre></body></html>")
            
            # === PDF / FALLBACK TXT ===
            else:
                # Real PDF processing libraries require external setup, wrapping as structured logs
                filepath = filepath.replace(".pdf", "_pdf_stream.txt")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"[PDF Export Simulation stream]\nModule: {self.module_name}\nData: {str(content_data)}")

            return filepath
        except Exception as e:
            print(Colors.fail(f"[-] Advanced report compilation failed: {e}"))
            return ""

def view_report_pipeline():
    """Workspace isolated viewer utility (Option 14)"""
    report_dir = "reports"
    print(f"\n{Colors.BLUE}[*] Isolated File Repositories inside local environment workspace:{Colors.RESET}")
    
    if not os.path.exists(report_dir) or not os.listdir(report_dir):
        print(Colors.fail("[-] No saved reports isolated in the workspace directory."))
        return
        
    files = os.listdir(report_dir)
    if not files:
        print(Colors.fail("[-] No compatible report assets found."))
        return

    for idx, file_name in enumerate(files, 1):
        print(f"  [{idx}] {file_name}")

    try:
        choice = input(f"\n{Colors.YELLOW}[?] Enter report number to read (or press Enter to cancel): ").strip()
        if not choice: return
        file_idx = int(choice) - 1
        if 0 <= file_idx < len(files):
            target_file = os.path.join(report_dir, files[file_idx])
            print(f"\n{Colors.GREEN}[=== READING ASSIGNED EXPORT ASSET: {files[file_idx]} ===]{Colors.RESET}\n")
            with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                print(f.read())
            print(f"\n{Colors.GREEN}[=== END OF REPORT EXECUTION DUMP ===]{Colors.RESET}\n")
    except Exception as e:
        print(Colors.fail(f"Execution handling failure: {e}"))