import base64
from core.colors import Colors
from core.report import ReportGenerator

def manage_base64() -> dict:
    print(f"\n{Colors.YELLOW}[1] Base64 Encode (Plaintext to Base64)")
    print(f"[2] Base64 Decode (Base64 to Plaintext)")
    sub_choice = input(f"{Colors.YELLOW}[?] Select Sub-Mode: ").strip()
    
    results = {}
    
    if sub_choice == "1":
        plaintext = input("\nEnter the plaintext data to Encode: ").strip()
        if not plaintext:
            print(Colors.fail("Error: Input cannot be empty."))
            return {}
        try:
            encoded_bytes = base64.b64encode(plaintext.encode('utf-8'))
            output_str = encoded_bytes.decode('utf-8')
            print(f"\n{Colors.GREEN}[=== ENCODE SUCCESS ===]")
            print(f"  [+] Original Text : {plaintext}")
            print(f"  [+] Base64 Output : {Colors.YELLOW}{output_str}\n")
            results = {"action": "encode", "input": plaintext, "output": output_str}
        except Exception as e:
            print(Colors.fail(f"Encoding issue: {e}"))

    elif sub_choice == "2":
        base64_string = input("\nEnter the Base64 string to Decode: ").strip()
        if not base64_string:
            print(Colors.fail("Error: Input cannot be empty."))
            return {}
        try:
            decoded_bytes = base64.b64decode(base64_string.encode('utf-8'))
            output_str = decoded_bytes.decode('utf-8')
            print(f"\n{Colors.GREEN}[=== DECODE SUCCESS ===]")
            print(f"  [+] Base64 String : {base64_string}")
            print(f"  [+] Plaintext     : {Colors.YELLOW}{output_str}\n")
            results = {"action": "decode", "input": base64_string, "output": output_str}
        except Exception:
            print(Colors.fail("\n[-] Decoding failed: Invalid structural formatting or illegal padding bits."))
            return {}
    else:
        print(Colors.fail("Invalid selection."))
        return {}

    # === REPORT ADVANCED EXPORT SYSTEM INTEGRATION ===
    if results:
        export_choice = input(f"{Colors.YELLOW}[?] Export report? (y/n): ").strip().lower()
        if export_choice == 'y':
            fmt = input("Format (txt, json, csv, html) [txt]: ").strip().lower() or "txt"
            # FIXED: Pass module target explicitly to secure initial initialization
            reporter = ReportGenerator("base64_tool")
            saved_path = reporter.write_report(results, fmt)
            if saved_path:
                print(f"{Colors.GREEN}[+] Output matrix successfully generated at: {saved_path}")
                
    return results