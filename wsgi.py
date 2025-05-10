"""
WSGI entry point for Gunicorn
"""

import os
import sys
# Add the parent directory of the script to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, configure_scheduler

if __name__ == "__main__":
    # Configure the scheduler when starting with Gunicorn
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        configure_scheduler()
    app.run()
