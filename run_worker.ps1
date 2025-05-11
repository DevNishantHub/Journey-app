# PowerShell script to run the background worker locally
# filepath: f:\Programming\Vibecoding\journey_app\run_worker.ps1

Write-Host "Starting DevOps Journey App background worker..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the worker" -ForegroundColor Yellow

# Change to the directory containing this script
Set-Location -Path $PSScriptRoot

# Run the worker script
python worker.py

Write-Host "Worker has been stopped." -ForegroundColor Red
