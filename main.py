"""
Wikipedia Talk Page Policy Analyzer - Main Entry Point

Professional Flask application for analyzing Wikipedia talk page discussions
and identifying policy, guideline, and essay mentions.

Author: Utkarsh Rai
Repository: https://github.com/UtkarshRai247/Wikipedia-v2
"""

import os
from app import create_app

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (for deployment) or use default
    port = int(os.environ.get('PORT', 5001))
    
    print("\n" + "="*60)
    print("Wikipedia Talk Page Policy Analyzer")
    print("="*60)
    print(f"Starting server on port {port}")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Run the Flask development server
    # Use 0.0.0.0 for deployment compatibility
    app.run(debug=False, port=port, host='0.0.0.0')
