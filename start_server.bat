@echo off
:: filepath: f:\Programming\Vibecoding\journey_app\start_server.bat
:: Windows batch script to start the Journey App with Gunicorn

echo Starting Journey App with Gunicorn...
echo Press Ctrl+C to stop the server

:: Change to the directory containing this script
cd /d "%~dp0"

:: Start Gunicorn with 4 worker processes
gunicorn --workers=4 --bind=0.0.0.0:5000 wsgi:app

echo Journey App server has been stopped.
