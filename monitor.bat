@echo off
:: 1. Navigate to the main pipeline folder
cd /d "C:\python\Portfolio"

:: 2. Activate the virtual environment from the NEW location
call "C:\Python\venv\Scripts\activate"


:: 3. Run scripts from the NEW /dags subfolder
python .\monitor_script.py


pause
