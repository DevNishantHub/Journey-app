# DevOps Journey App Deployment Guide

## Local Development

### Running with Flask Development Server
```pwsh
cd f:\Programming\Vibecoding\journey_app
python src\main.py
```

### Running with Gunicorn (Recommended for Testing Production)
```pwsh
cd f:\Programming\Vibecoding\journey_app
# PowerShell
.\start_server.ps1
# OR Command Prompt
start_server.bat
```

### Running the Background Worker
```pwsh
cd f:\Programming\Vibecoding\journey_app
# PowerShell
.\run_worker.ps1
# OR Command Prompt
run_worker.bat
```

## Deployment to Render.com

### Prerequisites
1. Push your code to a Git repository (GitHub, GitLab, etc.)
2. Create an account on [Render.com](https://render.com)

### Web Service Deployment
1. In Render dashboard, click "New" and select "Web Service"
2. Connect your Git repository
3. Configure the service:
   - **Name**: devops-journey-app (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11

### Background Worker Deployment
1. In Render dashboard, click "New" and select "Background Worker"
2. Connect your Git repository
3. Configure the service:
   - **Name**: devops-journey-worker (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python worker.py`
   - **Python Version**: 3.11

### Environment Variables
Make sure to set these environment variables in Render dashboard:
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SENDER_EMAIL`
- `RECEIVER_EMAIL`

## Troubleshooting

### Common Issues
1. **ModuleNotFoundError**:
   - Ensure your file structure matches what's expected in imports
   - Check that your virtual environment has all required packages

2. **Email Not Sending**:
   - Verify environment variables are set correctly
   - For Gmail, ensure you're using an App Password

3. **Scheduler Not Running**:
   - Check logs to ensure the scheduler is initializing
   - Verify your cron settings in the configure_scheduler() function
