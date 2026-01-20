"""
Flask Routes

All HTTP endpoints for the Wikipedia Policy Analyzer application.
"""

from flask import Blueprint, render_template, request, jsonify
from scrapers.wikitext_scraper import fetch_wikitext_section
from analyzers.policy_extractor import extract_wikipedia_links, format_policy_list_with_context
from analyzers.context_extractor import extract_all_policy_contexts
from analyzers.openai_analyzer import identify_policies_with_openai
from app.utils import add_highlight_ids

# Create blueprint
bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@bp.route('/favicon.ico')
def favicon():
    """Return empty favicon to prevent 404 errors"""
    return '', 204


@bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze Wikipedia discussion endpoint.
    
    Accepts a POST request with a URL to a Wikipedia talk page discussion,
    scrapes the specific discussion section, and analyzes it for policy/guideline/essay mentions.
    
    Request JSON:
        {
            "url": "https://en.wikipedia.org/wiki/Talk:Article#Section_Name"
        }
    
    Response JSON:
        {
            "discussion_html": "<html content of the specific discussion>",
            "policies": "Analysis of policies mentioned",
            "guidelines": "Analysis of guidelines mentioned", 
            "essays": "Analysis of essays mentioned"
        }
    """
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        


        print(f"\n{'='*60}")
        print(f"Starting analysis for: {url}")
        print(f"{'='*60}")
        
        # Scrape the specific discussion section using wikitext API
        print("Using wikitext API scraper...")
        discussion = fetch_wikitext_section(url)
        
        if not discussion:
            print("Error: Failed to scrape Wikipedia page")
            return jsonify({
                'error': 'Failed to scrape Wikipedia page. Please check the URL and try again.'
            }), 500
        
        print(f"\n✓ Successfully scraped discussion")
        print(f"  HTML length: {len(discussion['html'])} characters")
        print(f"  Text length: {len(discussion['text'])} characters")
        
        # Try to use OpenAI for analysis, fallback to pattern matching if unavailable
        import os
        if os.environ.get("OPENAI_API_KEY"):
            print(f"\nAnalyzing discussion with OpenAI...")
            openai_results = identify_policies_with_openai(discussion['text'])
            
            # The OpenAI results are already formatted HTML strings
            policies_html = openai_results['policies']
            guidelines_html = openai_results['guidelines']
            essays_html = openai_results['essays']
            
            # Use the original discussion HTML
            discussion_html_with_ids = discussion['html']
        else:
            # Fallback to pattern-based detection
            print(f"\nOpenAI API key not found. Using pattern-based detection...")
            extracted_links = extract_wikipedia_links(discussion['html'], discussion['text'])
            
            print(f"  Found {len(extracted_links['policies'])} policies")
            print(f"  Found {len(extracted_links['guidelines'])} guidelines")
            print(f"  Found {len(extracted_links['essays'])} essays")
            
            # Extract contexts for each policy/guideline/essay
            print(f"\nExtracting contexts for policy mentions...")
            with_contexts = extract_all_policy_contexts(
                discussion['text'],
                extracted_links['policies'],
                extracted_links['guidelines'],
                extracted_links['essays']
            )
            
            # Add IDs to discussion HTML for highlighting/scrolling
            discussion_html_with_ids = add_highlight_ids(
                discussion['html'], 
                with_contexts['policies'] + with_contexts['guidelines'] + with_contexts['essays']
            )
            
            # Format the results for display with context snippets
            policies_html = format_policy_list_with_context(with_contexts['policies'], 'policy')
            guidelines_html = format_policy_list_with_context(with_contexts['guidelines'], 'guideline')
            essays_html = format_policy_list_with_context(with_contexts['essays'], 'essay')
        
        print(f"\n✓ Analysis complete!")
        print(f"{'='*60}\n")
        
        return jsonify({
            'discussion_html': discussion_html_with_ids,
            'policies': policies_html,
            'guidelines': guidelines_html,
            'essays': essays_html
        })
        
    except Exception as e:
        print(f"\n✗ Error in analyze endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

