"""
WSGI Entry Point for Gunicorn

This file provides a clean entry point for Gunicorn deployment.
"""

import os
import sys

# Ensure the current directory is in the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Create the Flask app directly
try:
    from app import create_app
    application = create_app()
    app = application  # Alias for compatibility
except Exception as e:
    print(f"ERROR: Failed to create Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    application.run()
