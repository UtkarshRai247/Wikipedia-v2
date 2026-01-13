"""
Wikipedia Talk Page Scraper Module

This module handles scraping Wikipedia talk pages and extracting specific discussion sections.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import re


def scrape_wikipedia_discussion(url):
    """
    Scrape a specific discussion section from a Wikipedia talk page.
    
    Args:
        url: Full URL to the Wikipedia talk page discussion, optionally with section anchor
        
    Returns:
        dict with 'html' and 'text' keys containing the discussion content,
        or None if scraping fails
    """
    try:
        # Parse the URL to extract the section anchor if present
        parsed_url = urlparse(url)
        section_anchor = unquote(parsed_url.fragment) if parsed_url.fragment else None
        base_url = url.split('#')[0]  # Remove fragment for the request
        
        print(f"Fetching URL: {base_url}")
        if section_anchor:
            print(f"Target section: {section_anchor}")
        
        # Add proper headers to avoid being blocked by Wikipedia
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"Response status: {response.status_code}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content area
        content = soup.find('div', {'class': 'mw-parser-output'})
        
        if not content:
            print("Error: Could not find main content div with class 'mw-parser-output'")
            # Try alternative selector
            content = soup.find('div', {'id': 'mw-content-text'})
            if not content:
                print("Error: Could not find content with alternative selectors")
                return None
        
        # If a section anchor is provided, extract only that section
        if section_anchor:
            discussion_content = extract_section(content, section_anchor)
            if not discussion_content:
                print(f"Warning: Could not find section '{section_anchor}', falling back to full page")
                discussion_content = content
        else:
            discussion_content = content
        
        print(f"Found content, length: {len(str(discussion_content))} characters")
        
        # Extract discussion HTML and text
        discussion_html = str(discussion_content)
        discussion_text = discussion_content.get_text(separator='\n', strip=True)
        
        print(f"Extracted text length: {len(discussion_text)} characters")
        
        return {
            'html': discussion_html,
            'text': discussion_text
        }
    except requests.exceptions.RequestException as e:
        print(f"Request error scraping Wikipedia: {e}")
        return None
    except Exception as e:
        print(f"Error scraping Wikipedia: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_section(content_div, section_anchor):
    """
    Extract a specific section from Wikipedia talk page content.
    
    Wikipedia talk pages have sections marked by heading tags (h1-h6) with id attributes.
    This function finds the heading with the matching id and extracts all content
    until the next heading of the same or higher level.
    
    Args:
        content_div: BeautifulSoup element containing the page content
        section_anchor: The section anchor/id to extract (e.g., "Section_Name")
        
    Returns:
        BeautifulSoup element containing only the target section, or None if not found
    """
    try:
        # Find all headings in the content
        all_headings = content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        # Try to find the target heading by id or by matching the text
        target_heading = None
        target_index = -1
        
        for idx, heading in enumerate(all_headings):
            # Check if the heading id matches
            if heading.get('id') == section_anchor:
                target_heading = heading
                target_index = idx
                break
            
            # Also check if the anchor matches a span.mw-headline inside the heading
            headline = heading.find('span', {'class': 'mw-headline'})
            if headline and headline.get('id') == section_anchor:
                target_heading = heading
                target_index = idx
                break
        
        if not target_heading:
            print(f"Could not find heading with anchor: {section_anchor}")
            return None
        
        print(f"Found target heading: {target_heading.name} - {target_heading.get_text().strip()}")
        
        # Get the heading level (2 for h2, 3 for h3, etc.)
        target_level = int(target_heading.name[1])
        
        # Find the next heading of same or higher level (this is our boundary)
        next_heading = None
        if target_index < len(all_headings) - 1:
            for heading in all_headings[target_index + 1:]:
                heading_level = int(heading.name[1])
                if heading_level <= target_level:
                    next_heading = heading
                    print(f"Next section boundary: {heading.name} - {heading.get_text().strip()}")
                    break
        
        # Convert to string and extract using string positions
        full_html = str(content_div)
        target_heading_str = str(target_heading)
        
        # Find where our target heading appears in the HTML
        start_pos = full_html.find(target_heading_str)
        if start_pos == -1:
            print("Could not locate target heading in HTML")
            return None
        
        # Find where the next heading appears (or end of content)
        if next_heading:
            next_heading_str = str(next_heading)
            end_pos = full_html.find(next_heading_str, start_pos + len(target_heading_str))
            if end_pos == -1:
                end_pos = len(full_html)
        else:
            end_pos = len(full_html)
        
        # Extract the section HTML
        section_html = '<div class="extracted-section">' + full_html[start_pos:end_pos] + '</div>'
        
        result = BeautifulSoup(section_html, 'html.parser')
        print(f"Extracted section HTML length: {len(section_html)} characters")
        
        return result
        
    except Exception as e:
        print(f"Error extracting section: {e}")
        import traceback
        traceback.print_exc()
        return None


def clean_discussion_text(text):
    """
    Clean up discussion text by removing navigation elements, templates, etc.
    
    Args:
        text: Raw text extracted from the discussion
        
    Returns:
        Cleaned text suitable for analysis
    """
    # Remove common navigation/template text that appears on talk pages
    patterns_to_remove = [
        r'Retrieved from.*',
        r'Categories:.*',
        r'Hidden categories:.*',
        r'This page was last edited on.*',
        r'Text is available under.*',
        r'Privacy policy.*',
        r'About Wikipedia.*',
        r'Disclaimers.*',
    ]
    
    cleaned = text
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove excessive whitespace
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

