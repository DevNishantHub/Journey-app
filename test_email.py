import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
#hi


# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Email Configuration from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Validate email configuration
if not all([SMTP_SERVER, SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL, RECEIVER_EMAIL]):
    print("ERROR: Email configuration is incomplete. Please check your .env file.")
    print("Make sure you have the following environment variables set:")
    print("  - SMTP_SERVER: Your email server (e.g., smtp.gmail.com)")
    print("  - SMTP_PORT: Your email server port (default: 587)")
    print("  - SMTP_USERNAME: Your email username/address")
    print("  - SMTP_PASSWORD: Your email password or app password")
    print("  - SENDER_EMAIL: Email address to send from")
    print("  - RECEIVER_EMAIL: Email address to send to")

def send_test_email():
    """Send a simple test email"""
    print(f"Testing email send to {RECEIVER_EMAIL}")
    
    subject = f"Test Email - DevOps Journey ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
    
    # Create a simple HTML body
    html_content = f"""
    <html>
    <body>
        <h1>Test Email</h1>
        <p>This is a test email from your DevOps Journey application.</p>
        <p>Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>If you're seeing this, your email configuration is working correctly!</p>
    </body>
    </html>
    """
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    part_html = MIMEText(html_content, "html")
    msg.attach(part_html)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Use TLS
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"Email sent successfully to {RECEIVER_EMAIL}")
        return True, "Email sent successfully."
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication Error: {e}. Check credentials."
        print(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        print(error_msg)
        return False, error_msg

if __name__ == "__main__":
    print("=== Email Test Utility ===")
    result, message = send_test_email()
    print(f"Test completed. Result: {message}")
