"""
Entry point for Render.com deployment
Simply imports the application from the project
"""

from wsgi import application as app

# Render.com will look for an "app" variable in this file
