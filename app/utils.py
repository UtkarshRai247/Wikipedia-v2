"""
Utility Functions for the Flask Application

Helper functions for HTML processing, highlighting, etc.
"""

from bs4 import BeautifulSoup
import re


def add_highlight_ids(html_content, all_items):
    """
    Add unique IDs to the discussion HTML where policies are mentioned,
    so we can scroll to and highlight them.
    
    Args:
        html_content: The discussion HTML
        all_items: Combined list of policies, guidelines, and essays
        
    Returns:
        Modified HTML with highlight IDs added
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    for idx, item in enumerate(all_items):
        shortcut = item.get('shortcut')
        if not shortcut:
            continue
        
        # Find all text nodes containing the shortcut
        text_nodes = soup.find_all(string=re.compile(re.escape(shortcut)))
        
        for node in text_nodes:
            # Wrap the shortcut in a span with an ID
            highlight_id = f"highlight-{idx}"
            new_text = node.replace(
                shortcut,
                f'<span id="{highlight_id}" class="policy-mention">{shortcut}</span>'
            )
            
            # Replace the text node with parsed HTML
            new_soup = BeautifulSoup(new_text, 'html.parser')
            node.replace_with(new_soup)
            
            # Only highlight the first occurrence
            break
    
    return str(soup)

