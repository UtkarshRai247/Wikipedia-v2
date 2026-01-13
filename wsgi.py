"""
WSGI Entry Point for Gunicorn

This file provides a clean entry point for Gunicorn deployment.
"""

import os
import sys

# Ensure the current directory is in the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app
from main import app

# This is what Gunicorn will look for
application = app

if __name__ == "__main__":
    app.run()
