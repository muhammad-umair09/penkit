import base64
from core.colors import Colors

def process_base64(data: str, mode: str = "encode") -> dict:
    results = {"Mode": mode, "Input": data, "Output": ""}
    try:
        if mode == "encode":
            encoded_bytes = base64.b64encode(data.encode('utf-8'))
            results["Output"] = encoded_bytes.decode('utf-8')
            print(Colors.success(f"String converted: {results['Output']}"))
        else:
            decoded_bytes = base64.b64decode(data.encode('utf-8'))
            results["Output"] = decoded_bytes.decode('utf-8', errors='ignore')
            print(Colors.success(f"String parsed: {results['Output']}"))
    except Exception as e:
        results["Output"] = f"Action tracking failure: {str(e)}"
        print(Colors.fail("Transformer processing error occurred."))
    return results