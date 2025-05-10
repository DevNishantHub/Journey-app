import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import json
from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_apscheduler import APScheduler # Added for automated emails
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")
scheduler = APScheduler() # Initialize the scheduler

JOURNEY_DATA_PATH = os.path.join(os.path.dirname(__file__), "journey_data.json")

# Email Configuration - Must be set as environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587")) # Default to 587 (TLS) if port is specified
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Check if email configuration is present
if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL]):
    logger.warning("Email configuration is incomplete. Emails will not be sent.")
    logger.info("Please set the following environment variables:")
    logger.info("  - SMTP_SERVER: Your email server (e.g., smtp.gmail.com)")
    logger.info("  - SMTP_PORT: Your email server port (default: 587)")
    logger.info("  - SMTP_USERNAME: Your email username/address")
    logger.info("  - SMTP_PASSWORD: Your email password or app password")
    logger.info("  - SENDER_EMAIL: Email address to send from")
    logger.info("  - RECEIVER_EMAIL: Email address to send to")

def load_journey_data():
    try:
        with open(JOURNEY_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Error: {JOURNEY_DATA_PATH} not found.")
        return None
    except json.JSONDecodeError:
        logger.error(f"Error: Could not decode JSON from {JOURNEY_DATA_PATH}.")
        return None

def get_week_start_end_dates(week_dates_str):
    try:
        year_match = re.search(r'(\d{4})', week_dates_str)
        if not year_match:
            return None, None
        year = int(year_match.group(1))
        dates_no_year = week_dates_str.replace(f", {year}", "").strip()
        
        # Handle both en-dash and hyphen separators
        parts = dates_no_year.split('\u2013') # en-dash
        if len(parts) != 2:
            parts = dates_no_year.split('-') # hyphen
            if len(parts) != 2:
                return None, None

        start_str, end_str = parts[0].strip(), parts[1].strip()
        
        # Extract month name from start date if not present in end date
        start_month_match = re.match(r"([A-Za-z]+)", start_str)
        start_month = start_month_match.group(1) if start_month_match else ""
        
        # If end date has no month, add it from start date
        if not any(char.isalpha() for char in end_str):
            end_str = f"{start_month} {end_str}"
        
        # Construct full date strings with year
        start_date_str_full = f"{start_str} {year}"
        end_date_str_full = f"{end_str} {year}"
        
        # Try different date formats for both start and end dates
        date_formats = ["%b %d %Y", "%B %d %Y"]
        
        # Parse start date
        start_date = None
        for fmt in date_formats:
            try:
                start_date = datetime.strptime(start_date_str_full, fmt)
                break
            except ValueError:
                continue
                
        if not start_date:
            raise ValueError(f"Could not parse start date: {start_date_str_full}")
            
        # Parse end date
        end_date = None
        for fmt in date_formats:
            try:
                end_date = datetime.strptime(end_date_str_full, fmt)
                break
            except ValueError:
                continue
                
        if not end_date:
            raise ValueError(f"Could not parse end date: {end_date_str_full}")
            
        return start_date, end_date
    except Exception as e:
        logger.error(f"Error parsing date string '{week_dates_str}': {e}")
        return None, None

def get_todays_tasks(journey_data):
    if not journey_data or "phases" not in journey_data:
        return []

    today = datetime.now()
    # today = datetime(2025, 5, 12) # For testing specific dates

    todays_tasks_list = []

    for phase in journey_data["phases"]:
        for week in phase.get("weeks", []):
            start_date, end_date = get_week_start_end_dates(week.get("dates", ""))
            if start_date and end_date:
                end_date_inclusive = end_date + timedelta(days=1)
                if start_date <= today < end_date_inclusive:
                    task_info = {
                        "phase_name": phase.get("name", "N/A"),
                        "week_focus": week.get("focus", "N/A"),
                        "week_dates": week.get("dates", "N/A"),
                        "tasks": week.get("tasks", [])
                    }
                    if not task_info["tasks"]:
                         task_info["tasks"].append(f"Focus on: {week.get('description', week.get('focus', 'current topics'))}")
                    todays_tasks_list.append(task_info)
    
    if not todays_tasks_list and journey_data.get("ongoing_learning"):
        ongoing_info = journey_data["ongoing_learning"]
        duration_overall = ongoing_info.get("duration_overall", "")
        if duration_overall and " \u2013 " in duration_overall:
            ongoing_start_str, ongoing_end_str = duration_overall.split(" \u2013 ")
            try:
                # Attempt to parse ongoing start/end dates with improved handling for various formats
                # Normalize the date strings first (remove ordinal suffixes, ensure correct spacing)
                ongoing_start_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", ongoing_start_str.strip())
                ongoing_end_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", ongoing_end_str.strip())
                
                # Try multiple date formats for both start and end dates
                date_formats_to_try = [
                    "%b %d, %Y",  # Aug 12, 2025
                    "%b %d %Y",   # Aug 12 2025
                    "%B %d, %Y",  # August 12, 2025
                    "%B %d %Y"    # August 12 2025
                ]
                
                # Parse start date
                ongoing_start_date = None
                for fmt in date_formats_to_try:
                    try:
                        ongoing_start_date = datetime.strptime(ongoing_start_str, fmt)
                        break
                    except ValueError:
                        continue
                
                if not ongoing_start_date:
                    raise ValueError(f"Could not parse ongoing start date: {ongoing_start_str}")
                
                # Parse end date
                ongoing_end_date = None
                for fmt in date_formats_to_try:
                    try:
                        ongoing_end_date = datetime.strptime(ongoing_end_str, fmt)
                        break
                    except ValueError:
                        continue
                
                if not ongoing_end_date:
                    raise ValueError(f"Could not parse ongoing end date: {ongoing_end_str}")
                
                if ongoing_start_date <= today <= ongoing_end_date + timedelta(days=1):
                    for period in ongoing_info.get("periods", []):
                        todays_tasks_list.append({
                            "phase_name": ongoing_info.get("title", "Ongoing Learning"),
                            "week_focus": period.get("focus", "N/A"),
                            "week_dates": period.get("dates", "N/A"),
                            "tasks": [period.get("focus", "Continue with ongoing learning topics.")]
                        })
                    if not todays_tasks_list:
                         todays_tasks_list.append({
                            "phase_name": ongoing_info.get("title", "Ongoing Learning"),
                            "week_focus": "General ongoing studies",
                            "week_dates": ongoing_info.get("duration_overall", "N/A"),
                            "tasks": [ongoing_info.get("description", "Focus on advanced topics and projects.")]
                        })
            except Exception as e:
                logger.error(f"Error parsing ongoing learning dates ('{duration_overall}'): {e}")

    return todays_tasks_list

def send_email(subject, html_content, to_email):
    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, to_email]) or \
       any(val.startswith("your_") or val.startswith("user_") for val in [SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, to_email]):
        logger.warning("SMTP configuration is incomplete or uses placeholder values. Email not sent.")
        logger.debug(f"DEBUG: Would send to {to_email} with subject: {subject}")
        # logger.debug(f"DEBUG: HTML Content:\n{html_content}") # Be careful with logging full email content
        return False, "SMTP configuration incomplete or uses placeholder values. Check environment variables."

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    part_html = MIMEText(html_content, "html")
    msg.attach(part_html)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls() # Use TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        logger.info(f"Email sent successfully to {to_email}")
        return True, "Email sent successfully."
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication Error: {e}. Check credentials."
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        logger.error(error_msg)
        return False, error_msg

def send_daily_reminder():
    """
    Function to be called by the scheduler every day.
    Sends daily reminder emails with tasks for the day.
    """
    logger.info(f"[{datetime.now()}] Running scheduled daily reminder...")
    journey = load_journey_data()
    if journey is None:
        logger.error("Error: Could not load journey data for scheduled reminder")
        return
    
    tasks = get_todays_tasks(journey)
    if not tasks:
        logger.info("No specific tasks for today according to the roadmap. No scheduled email sent.")
        return
    
    email_subject = f"Your DevOps Journey Reminder - {datetime.now().strftime('%Y-%m-%d')}"
    html_body = render_template("email_template.html", tasks_for_today=tasks)
    
    success, message = send_email(email_subject, html_body, RECEIVER_EMAIL)
    logger.info(f"Scheduled email result: {message}")

# Configure scheduler
def configure_scheduler():
    # Send email daily at 8:00 AM
    scheduler.add_job(id='send_daily_reminder', 
                     func=send_daily_reminder, 
                     trigger='cron', 
                     hour=8, 
                     minute=00)
    scheduler.start()
    
    logger.info(f"Scheduler started. Daily reminders will be sent at 8:00 AM to {RECEIVER_EMAIL}")

@app.route('/')
def home():
    journey = load_journey_data()
    if journey is None:
        return "Error loading journey data. Please check the logs.", 500
    return render_template("index.html", journey=journey)

@app.route('/api/today')
def api_today():
    journey = load_journey_data()
    if journey is None:
        return jsonify({"error": "Could not load journey data"}), 500
    tasks_for_today = get_todays_tasks(journey)
    return jsonify(tasks_for_today)

@app.route('/send-daily-reminder')
def send_daily_reminder_route():
    journey = load_journey_data()
    if journey is None:
        return jsonify({"status": "error", "message": "Could not load journey data for reminder"}), 500
    
    tasks = get_todays_tasks(journey)
    if not tasks:
        return jsonify({"status": "success", "message": "No specific tasks for today according to the roadmap. No email sent."}) 

    email_subject = f"Your DevOps Journey Reminder - {datetime.now().strftime('%Y-%m-%d')}"
    html_body = render_template("email_template.html", tasks_for_today=tasks)
    
    success, message = send_email(email_subject, html_body, RECEIVER_EMAIL)
    
    if success:
        return jsonify({"status": "success", "message": message})
    else:
        return jsonify({"status": "error", "message": message}), 500

if __name__ == '__main__':
    # Prevent scheduler from running twice in debug mode
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        configure_scheduler()
    app.run(host="0.0.0.0", port=5000, debug=True)

