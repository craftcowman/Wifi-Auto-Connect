@echo off
cd /d "%~dp0"
py -m pip install pyinstaller
py -m PyInstaller --onefile --noconsole --clean --name WiFiAutoConnect wifi_connect.py
echo.
echo Your single EXE is:
echo %~dp0dist\WiFiAutoConnect.exe
pause
