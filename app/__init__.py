"""
Flask Application Package

This package contains the main Flask application, routes, and utilities.
"""

from flask import Flask
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    """
    Application factory pattern for creating Flask app.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app

