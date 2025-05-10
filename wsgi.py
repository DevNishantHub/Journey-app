"""
WSGI entry point for Gunicorn
"""

import os
import sys
# Add the parent directory of the script to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app, configure_scheduler

# Configure the scheduler when Gunicorn starts
if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    configure_scheduler()

# This is the application object that Gunicorn will use
application = app

# For compatibility with different WSGI servers
wsgi_app = application
