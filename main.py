#!/usr/bin/env python3
"""
Wikipedia Talk Page Policy Analyzer - Main Entry Point

Professional Flask application for analyzing Wikipedia talk page discussions
and identifying policy, guideline, and essay mentions.

Usage:
  # Start web server (default)
  python main.py
  python main.py server --port 5001

  # Export analysis to Google Sheets format
  python main.py export --url "https://en.wikipedia.org/wiki/Talk:Article#Section"
  python main.py export --url "..." --output results.tsv
  python main.py export --url "..." --format csv

Author: Utkarsh Rai
Repository: https://github.com/YEETlord247/WIkipedia-Policy-Scraping
"""

import argparse
import sys
import os


def run_server(port=5001):
    """Start Flask development server"""
    from app import create_app
    app = create_app()

    print("\n" + "="*60)
    print("Wikipedia Talk Page Policy Analyzer")
    print("="*60)
    print(f"Starting server on port {port}")
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")

    app.run(debug=False, port=port, host='0.0.0.0')


def main():
    parser = argparse.ArgumentParser(
        description='Wikipedia Talk Page Policy Analyzer',
        epilog='Run without arguments to start web server'
    )

    # Optional command (defaults to server if not specified)
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Server command
    server_parser = subparsers.add_parser('server', help='Start web server (default)')
    server_parser.add_argument('--port', type=int, default=None,
                              help='Port to run server on (default: 5001 or PORT env var)')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export analysis to Google Sheets format')
    export_parser.add_argument('--url', required=True, help='Wikipedia talk page URL')
    export_parser.add_argument('--output', '-o', help='Output file (default: print to stdout)')
    export_parser.add_argument('--format', choices=['tsv', 'csv', 'json'], default='tsv',
                              help='Output format (default: tsv)')

    args = parser.parse_args()

    # Handle commands
    if args.command == 'export':
        # Import here to avoid loading web app dependencies for export
        from cli.export_command import run_export
        run_export(args.url, args.output, args.format)

    elif args.command == 'server':
        # Use specified port or environment variable or default
        port = args.port if args.port else int(os.environ.get('PORT', 5001))
        run_server(port)

    else:
        # No command specified: default to server (backward compatibility)
        # Use environment variable or default port
        port = int(os.environ.get('PORT', 5001))
        run_server(port)


if __name__ == '__main__':
    main()
