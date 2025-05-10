# PowerShell script to start the Journey App with Gunicorn

Write-Host "Starting Journey App with Gunicorn..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow

# Change to the directory containing this script
Set-Location -Path $PSScriptRoot

# Start Gunicorn with 4 worker processes
gunicorn --workers=4 --bind=0.0.0.0:5000 wsgi:app

Write-Host "Journey App server has been stopped." -ForegroundColor Red
