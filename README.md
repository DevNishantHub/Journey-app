# DevOps Journey Tracker Web Application

This web application helps you track your DevOps learning journey, based on the provided roadmap. It displays the full journey, highlights current tasks, and includes a feature to send daily email reminders for what you need to do today. It also features a simple Three.js visualization.

## Features

*   **Journey Display**: View your entire DevOps learning roadmap, broken down by phases and weeks.
*   **Today's Tasks**: The application can identify and (via email) list tasks relevant to the current date based on the roadmap.
*   **Email Reminders**: Manually trigger an email reminder for today's tasks.
*   **Three.js Visualization**: A simple 3D cube animation on the main page.
*   **Minimal File Structure**: Designed for easier maintenance.

## Project Structure

```
journey_app/
├── src/
│   ├── models/           # (Currently unused, for potential future database integration)
│   ├── routes/           # (Currently unused, for potential future API route expansion)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── main_app.js
│   │       └── three_visualization.js
│   ├── templates/
│   │   ├── email_template.html
│   │   └── index.html
│   ├── journey_data.json # Parsed roadmap data
│   └── main.py           # Main Flask application logic
├── venv/                 # Python virtual environment
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Setup and Installation

1.  **Clone/Download:** Get the project files onto your local machine.
2.  **Python Environment:**
    *   It's highly recommended to use a Python virtual environment.
    *   If you have `python3.11` (or a compatible Python 3 version) and `pip`:
        ```bash
        cd journey_app
        python3 -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        pip install -r requirements.txt
        ```

3.  **Configure Email Reminders (Environment Variables):**
    For the email reminder functionality to work, you need to set the following environment variables before running the application. These are typically set in your shell session or a `.env` file (if you choose to use a library like `python-dotenv`, which is not included by default).

    *   `SMTP_SERVER`: Your SMTP server address (e.g., `smtp.gmail.com`).
    *   `SMTP_PORT`: Your SMTP server port (e.g., `587` for TLS, `465` for SSL).
    *   `SMTP_USERNAME`: Your email address for SMTP authentication.
    *   `SMTP_PASSWORD`: Your email password or an app-specific password (recommended for services like Gmail).
    *   `SENDER_EMAIL`: The email address from which reminders will be sent (usually the same as `SMTP_USERNAME`).
    *   `RECEIVER_EMAIL`: The email address where you want to receive the daily reminders.

    **Example (bash/zsh):**
    ```bash
    export SMTP_SERVER="smtp.example.com"
    export SMTP_PORT="587"
    export SMTP_USERNAME="your_email@example.com"
    export SMTP_PASSWORD="your_super_secret_password"
    export SENDER_EMAIL="your_email@example.com"
    export RECEIVER_EMAIL="your_personal_email@example.com"
    ```

## Running the Application

1.  **Activate Virtual Environment:**
    ```bash
    cd journey_app
    source venv/bin/activate # Or venv\Scripts\activate on Windows
    ```
2.  **Set Environment Variables:** Ensure your SMTP environment variables are set as described above.
3.  **Run Flask App:**
    ```bash
    python src/main.py
    ```
4.  **Access the Application:** Open your web browser and go to `http://127.0.0.1:5000`.

## Daily Email Reminders

*   **Manual Trigger:** To receive an email reminder for today's tasks, open your browser and navigate to:
    `http://127.0.0.1:5000/send-daily-reminder`
    This will trigger the email sending process if your SMTP settings are correctly configured.

*   **Automated Scheduling (External):**
    This application itself does not include a built-in scheduler for automatic daily emails due to system limitations of the environment it was developed in. However, you can easily set this up using an external scheduler like `cron` (on Linux/macOS) or Task Scheduler (on Windows) to call the `/send-daily-reminder` URL every morning.

    **Example using `cron` (Linux/macOS):**
    1.  Open your crontab for editing: `crontab -e`
    2.  Add a line to trigger the reminder, for example, every day at 8:00 AM:
        ```cron
        0 8 * * * curl http://127.0.0.1:5000/send-daily-reminder > /dev/null 2>&1
        ```
        (Ensure the Flask application is running when the cron job executes, or deploy it as a persistent service.)

    **Note:** If your application is not running on `127.0.0.1:5000` (e.g., if it's deployed elsewhere), replace the URL in the `curl` command accordingly.

## Customization

*   **Journey Data**: The learning roadmap is stored in `src/journey_data.json`. You can modify this file if your journey changes, but ensure you maintain the existing JSON structure for the application to parse it correctly.
*   **Styling**: Modify `src/static/css/style.css` for visual changes.
*   **Three.js**: The 3D visualization logic is in `src/static/js/three_visualization.js`.

## Technologies Used

*   **Backend**: Flask (Python)
*   **Frontend**: HTML, CSS, JavaScript
*   **3D Graphics**: Three.js
*   **Data Format**: JSON

Let me know if you have any questions or need further assistance!
# Journey-app
# Journey-app
