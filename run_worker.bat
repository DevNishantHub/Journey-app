@echo off
:: filepath: f:\Programming\Vibecoding\journey_app\run_worker.bat
:: Windows batch script to run the background worker locally

echo Starting DevOps Journey App background worker...
echo Press Ctrl+C to stop the worker

:: Change to the directory containing this script
cd /d "%~dp0"

:: Run the worker script
python worker.py

echo Worker has been stopped.
