import os
import json
import csv
from datetime import datetime
from typing import Any, Dict
from fpdf import FPDF
from core.colors import Colors

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export(self, module_name: str, target: str, data: Dict[str, Any], fmt: str = "json") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_target = target.replace("http://", "").replace("https://", "").replace("/", "_")
        filename = f"{module_name}_{sanitized_target}_{timestamp}"
        
        fmt = fmt.lower()
        if fmt == "json":
            return self._to_json(filename, data)
        elif fmt == "csv":
            return self._to_csv(filename, data)
        elif fmt == "html":
            return self._to_html(filename, module_name, target, data)
        elif fmt == "pdf":
            return self._to_pdf(filename, module_name, target, data)
        else:
            return self._to_txt(filename, data)

    def _to_txt(self, filename: str, data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, f"{filename}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"PenKit Analysis Report\nGenerated: {datetime.now()}\n")
            f.write("="*50 + "\n")
            for k, v in data.items():
                f.write(f"{k}: {v}\n")
        return filepath

    def _to_json(self, filename: str, data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        payload = {
            "meta": {"engine": "PenKit", "timestamp": str(datetime.now())},
            "results": data
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
        return filepath

    def _to_csv(self, filename: str, data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, f"{filename}.csv")
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Metric / Key", "Value / Observation"])
            for k, v in data.items():
                writer.writerow([k, str(v)])
        return filepath

    def _to_html(self, filename: str, module: str, target: str, data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, f"{filename}.html")
        rows = "".join([f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>" for k, v in data.items()])
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 30px; background-color: #f4f6f9; color: #333; }}
                h1 {{ color: #1e293b; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: #fff; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #0f172a; color: white; }}
                tr:hover {{ background-color: #f1f5f9; }}
            </style>
        </head>
        <body>
            <h1>PenKit Assessment Report</h1>
            <p><strong>Module:</strong> {module} | <strong>Target:</strong> {target} | <strong>Execution Time:</strong> {datetime.now()}</p>
            <table>
                <tr><th>Parameter</th><th>Value</th></tr>
                {rows}
            </table>
        </body>
        </html>
        """
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath

    def _to_pdf(self, filename: str, module: str, target: str, data: Dict[str, Any]) -> str:
        filepath = os.path.join(self.output_dir, f"{filename}.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=14)
        pdf.cell(200, 10, txt="PenKit Assessment Report", ln=1, align="C")
        pdf.set_font("Helvetica", size=10)
        pdf.cell(200, 10, txt=f"Target: {target} | Module: {module} | Date: {datetime.now()}", ln=2, align="L")
        pdf.ln(5)
        
        pdf.set_font("Helvetica", size=9)
        for k, v in data.items():
            line = f"{k}: {str(v)}"
            # Handle basic encoding sanitization for FPDF
            line = line.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 6, txt=line)
        pdf.output(filepath)
        return filepath