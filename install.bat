@echo off
echo [*] Bootstrapping local runtime compilation pipeline...
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
echo [+] Automation setups complete. Launch toolkit running: python main.py
pause