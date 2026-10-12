@echo off
rem Windows: double-click to start the study app (opens your browser). Needs Python 3.8+ from python.org.
cd /d "%~dp0"
where py >nul 2>nul && (py -3 app\serve.py --open) || (python app\serve.py --open)
pause
