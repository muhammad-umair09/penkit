#!/bin/bash
echo "[*] Configuring PenKit Virtual Workstation Dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "[+] Project dependencies successfully set up. Execute via: python main.py"