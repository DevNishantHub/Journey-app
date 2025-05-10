import os
import sys
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "nishantkumar.iitmjp@gmail.com"
SMTP_PASSWORD = "Yadav@2207"
SENDER_EMAIL = "nishantkumar.iitmjp@gmail.com"
RECEIVER_EMAIL = "nishantkumar211106@gmail.com"

def test_send_email():
    """Test sending a simple email"""
    print(f"Testing email send to {RECEIVER_EMAIL}")
    
    subject = f"Test Email - DevOps Journey ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    # Create a simple HTML body
    simple_html = f"""
    <html>
    <body>
        <h1>Test Email</h1>
        <p>This is a test email from your DevOps Journey application.</p>
        <p>Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>If you're seeing this, your email configuration is working correctly!</p>
    </body>
    </html>
    """
    
    success, message = send_email(subject, simple_html, RECEIVER_EMAIL)
    print(f"Email send result: {message}")
    return success, message

def test_template_email():
    """Test sending an email with the actual template"""
    with app.app_context():
        print(f"Testing template email to {RECEIVER_EMAIL}")
        
        # Load journey data
        journey_data = load_journey_data()
        if not journey_data:
            print("Error: Failed to load journey data")
            return False, "Failed to load journey data"
        
        # Get today's tasks
        tasks = get_todays_tasks(journey_data)
        if not tasks:
            print("Warning: No tasks found for today")
            # Create a sample task for testing
            tasks = [{
                "phase_name": "Test Phase",
                "week_focus": "Test Focus",
                "week_dates": "May 1-10, 2025",
                "tasks": ["This is a test task", "Another test task"]
            }]
        
        subject = f"Test Template Email - DevOps Journey ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        try:
            # Render the email template
            html_body = render_template("email_template.html", tasks_for_today=tasks)
            
            # Send the email
            success, message = send_email(subject, html_body, RECEIVER_EMAIL)
            print(f"Template email send result: {message}")
            return success, message
        except Exception as e:
            print(f"Error when sending template email: {e}")
            return False, str(e)

if __name__ == "__main__":
    print("=== Email Test Utility ===")
    print("1. Testing simple email...")
    test_send_email()
    
    print("\n2. Testing template email...")
    test_template_email()
    
    print("\nTests completed.")
