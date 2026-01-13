"""
Wikipedia Wikitext Scraper

This module uses Wikipedia's API to fetch raw wikitext directly,
which is much faster and more reliable than HTML scraping.
"""

import requests
import re
from urllib.parse import urlparse, unquote


def fetch_wikitext_section(url):
    """
    Fetch raw wikitext for a specific section from Wikipedia's API.
    
    This is much more efficient than HTML scraping because:
    - Direct API access (no HTML parsing overhead)
    - Gets structured wikitext data
    - Faster response times
    - More reliable
    
    Args:
        url: Full URL to Wikipedia talk page, optionally with #section anchor
        
    Returns:
        dict with 'wikitext' and 'html' (for display) keys, or None if failed
    """
    try:
        # Parse the URL
        parsed_url = urlparse(url)
        section_anchor = unquote(parsed_url.fragment) if parsed_url.fragment else None
        
        # Extract page title from URL
        # Example: /wiki/Talk:Article_Name -> Talk:Article_Name
        path_parts = parsed_url.path.split('/wiki/')
        if len(path_parts) < 2:
            print(f"Invalid Wikipedia URL: {url}")
            return None
        
        page_title = unquote(path_parts[1])
        print(f"Fetching wikitext for page: {page_title}")
        if section_anchor:
            print(f"Target section: {section_anchor}")
        
        # Wikipedia API endpoint
        api_url = "https://en.wikipedia.org/w/api.php"
        
        # Wikipedia requires a User-Agent header
        headers = {
            'User-Agent': 'WikipediaPolicyAnalyzer/1.0 (Educational Research Tool; Contact: github.com/YEETlord247)',
            'Accept': 'application/json'
        }
        
        # Step 1: Get the full page wikitext
        params = {
            'action': 'parse',
            'page': page_title,
            'prop': 'wikitext|sections',
            'format': 'json',
            'formatversion': 2
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'error' in data:
            print(f"Wikipedia API error: {data['error']}")
            return None
        
        if 'parse' not in data:
            print("No parse data in API response")
            return None
        
        full_wikitext = data['parse']['wikitext']
        sections = data['parse'].get('sections', [])
        
        # Step 2: Extract specific section if anchor provided
        if section_anchor:
            section_wikitext = extract_section_from_wikitext(
                full_wikitext, 
                section_anchor, 
                sections
            )
            if not section_wikitext:
                print(f"Could not find section '{section_anchor}', using full page")
                section_wikitext = full_wikitext
        else:
            section_wikitext = full_wikitext
        
        # Step 3: Convert wikitext to HTML for display
        html_content = wikitext_to_html(section_wikitext, page_title)
        
        print(f"Successfully fetched {len(section_wikitext)} characters of wikitext")
        
        return {
            'wikitext': section_wikitext,
            'html': html_content,
            'text': wikitext_to_plain_text(section_wikitext)
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching wikitext: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_section_from_wikitext(wikitext, section_anchor, sections):
    """
    Extract a specific section from wikitext using section metadata.
    
    Args:
        wikitext: Full page wikitext
        section_anchor: The section anchor (e.g., "RfC_self-published_cartoon")
        sections: List of section metadata from Wikipedia API
        
    Returns:
        Extracted section wikitext or None
    """
    try:
        # Find the target section in metadata
        target_section = None
        for section in sections:
            # Check if anchor matches (with underscores converted to spaces and vice versa)
            section_id = section.get('anchor', '')
            if section_id == section_anchor or section_id.replace('_', ' ') == section_anchor.replace('_', ' '):
                target_section = section
                break
        
        if not target_section:
            print(f"Section '{section_anchor}' not found in section list")
            return None
        
        # Find section boundaries using heading markers
        section_level = target_section['level']
        section_line = target_section['line']  # The heading text
        
        # Create regex to find the section heading
        # Wikitext headings look like: == Heading ==, === Heading ===, etc.
        heading_pattern = re.escape(section_line)
        
        # Find the section start
        section_regex = r'^=+\s*' + heading_pattern + r'\s*=+\s*$'
        match = re.search(section_regex, wikitext, re.MULTILINE)
        
        if not match:
            print(f"Could not find heading '{section_line}' in wikitext")
            return None
        
        start_pos = match.start()
        
        # Find the next heading of equal or higher level (fewer = signs)
        # Level 2 = ==, Level 3 = ===, etc.
        next_heading_pattern = r'^={1,' + str(section_level) + r'}\s+.+?\s+={1,' + str(section_level) + r'}\s*$'
        
        # Search for next section after our target
        rest_of_text = wikitext[match.end():]
        next_match = re.search(next_heading_pattern, rest_of_text, re.MULTILINE)
        
        if next_match:
            # Extract up to the next section
            end_pos = match.end() + next_match.start()
            section_wikitext = wikitext[start_pos:end_pos]
        else:
            # This is the last section, take everything
            section_wikitext = wikitext[start_pos:]
        
        return section_wikitext.strip()
        
    except Exception as e:
        print(f"Error extracting section: {e}")
        import traceback
        traceback.print_exc()
        return None

"""
convert wikitext to html

Args:
    wikitext to HTML using wikipedia's API
    wikitext: Raw wikitext content
    Page_title: Page title for context

Returns:
    HTML string
    'User-Agent': 'WikipediaPolicyAnalyzer/1.0 (Educational Research Tool; Contact: github.com/YEETlord247)',
    'Accept': 'application/json'
    'contentmodel': 'wikitext'
    'format': 'json'
    'formatversion': 2
    'prop': 'text'
    'title': page_title
    'action': 'parse'
    'parse': 'wikitext'
    'parse': 'text'
    'parse': 'html'

Example:
    wikitext_to_html("== Heading ==", "Page Title")
    returns:
    <div class="extracted-section">
        <h2>Heading</h2>
        <p>Content</p>
    </div>

Errors:
    - If the wikitext is not valid, returns the wikitext wrapped in a pre tag
    - If the page title is not valid, returns the wikitext wrapped in a pre tag
    - If the API request fails, returns the wikitext wrapped in a pre tag
    - If the API response is not valid, returns the wikitext wrapped in a pre tag
    - If the API response is not valid, returns the wikitext wrapped in a pre tag
    - If the API response is not valid, returns the wikitext wrapped in a pre tag
"""

def wikitext_to_html(wikitext, page_title):
    """
    Convert wikitext to HTML using Wikipedia's API.
    
    Args:
        wikitext: Raw wikitext content
        page_title: Page title for context
        
    Returns:
        HTML string
    """
    try:
        api_url = "https://en.wikipedia.org/w/api.php"
        
        # Wikipedia requires a User-Agent header
        headers = {
            'User-Agent': 'WikipediaPolicyAnalyzer/1.0 (Educational Research Tool; Contact: github.com/YEETlord247)',
            'Accept': 'application/json'
        }
        
        params = {
            'action': 'parse',
            'text': wikitext,
            'title': page_title,
            'prop': 'text',
            'format': 'json',
            'formatversion': 2,
            'contentmodel': 'wikitext'
        }
        
        response = requests.post(api_url, data=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'parse' in data and 'text' in data['parse']:
            return data['parse']['text']
        
        return wikitext  # Fallback to raw wikitext
        
    except Exception as e:
        print(f"Error converting wikitext to HTML: {e}")
        # Fallback: return wikitext wrapped in pre tag
        return f'<pre>{wikitext}</pre>'


def wikitext_to_plain_text(wikitext):
    """
    Convert wikitext to plain text for analysis.
    
    Args:
        wikitext: Raw wikitext content
        
    Returns:
        Plain text string
    """
    # Remove wikitext formatting
    text = wikitext
    
    # Remove templates: {{template}}
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    
    # Remove links but keep text: [[link|text]] -> text, [[link]] -> link
    text = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', text)  # [[link|text]]
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)  # [[link]]
    
    # Remove external links: [http://example.com text] -> text
    text = re.sub(r'\[https?://[^\s\]]+\s+([^\]]+)\]', r'\1', text)
    text = re.sub(r'\[https?://[^\]]+\]', '', text)
    
    # Remove formatting: '''bold''', ''italic''
    text = re.sub(r"'''([^']+)'''", r'\1', text)
    text = re.sub(r"''([^']+)''", r'\1', text)
    
    # Remove heading markers: == Heading ==
    text = re.sub(r'^=+\s*(.+?)\s*=+\s*$', r'\1', text, flags=re.MULTILINE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Convert Wikipedia talk page indentation (colons) to spaces
    # Each colon at the start of a line represents one indentation level
    # Replace with 2 spaces per indentation level for readability
    def convert_indentation(match):
        colon_count = len(match.group(1))
        indent = '  ' * colon_count  # 2 spaces per level
        return indent + match.group(2)
    
    text = re.sub(r'^(:+)(.*)$', convert_indentation, text, flags=re.MULTILINE)
    
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

