@echo off
echo Starting Vault Audit Web Application...
echo.
echo Opening browser at http://localhost:5000
echo.
start http://localhost:5000
cd vault_audit
python app.py
pause