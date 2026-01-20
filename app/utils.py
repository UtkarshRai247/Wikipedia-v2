"""
Utility Functions for the Flask Application

Helper functions for HTML processing, highlighting, etc.
"""

from bs4 import BeautifulSoup
import re
import html


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


def process_llm_output_for_highlighting(llm_html, discussion_html):
    """
    Process LLM output HTML to add highlighting support.
    
    Extracts policy shortcuts from LLM output, finds them in discussion HTML,
    adds IDs for highlighting, and adds data-highlight attributes to LLM links.
    
    Args:
        llm_html: HTML string from LLM (policies, guidelines, or essays)
        discussion_html: The discussion HTML to add IDs to
        
    Returns:
        tuple: (modified_llm_html, modified_discussion_html, shortcuts_found)
    """
    if not llm_html or "No " in llm_html and "mentioned" in llm_html:
        return llm_html, discussion_html, []
    
    soup = BeautifulSoup(llm_html, 'html.parser')
    discussion_soup = BeautifulSoup(discussion_html, 'html.parser')
    
    shortcuts_found = []
    
    # Find all Wikipedia policy links in the LLM output
    policy_links = soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:'))
    
    for link in policy_links:
        # Extract the shortcut from the link text (e.g., "WP:NPOV" or "WP:NPOV (WEIGHT/UNDUE)")
        link_text = link.get_text()
        
        # Extract base shortcut (e.g., "WP:NPOV" from "WP:NPOV (WEIGHT/UNDUE)")
        match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
        if match:
            shortcut = match.group(1)
            shortcuts_found.append(shortcut)
    
    return llm_html, discussion_html, shortcuts_found


def add_highlighting_to_llm_results(policies_html, guidelines_html, essays_html, discussion_html):
    """
    Add highlighting and scrolling support to LLM-generated results.
    
    Args:
        policies_html: LLM output for policies
        guidelines_html: LLM output for guidelines  
        essays_html: LLM output for essays
        discussion_html: Original discussion HTML
        
    Returns:
        tuple: (modified_policies_html, modified_guidelines_html, modified_essays_html, modified_discussion_html)
    """
    discussion_soup = BeautifulSoup(discussion_html, 'html.parser')
    
    # Collect all shortcuts from all categories
    all_shortcuts = []
    
    # Process policies
    policies_soup = BeautifulSoup(policies_html, 'html.parser')
    for link in policies_soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
        link_text = link.get_text()
        match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
        if match:
            all_shortcuts.append(match.group(1))
    
    # Process guidelines
    guidelines_soup = BeautifulSoup(guidelines_html, 'html.parser')
    for link in guidelines_soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
        link_text = link.get_text()
        match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
        if match:
            all_shortcuts.append(match.group(1))
    
    # Process essays
    essays_soup = BeautifulSoup(essays_html, 'html.parser')
    for link in essays_soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
        link_text = link.get_text()
        match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
        if match:
            all_shortcuts.append(match.group(1))
    
    # Add IDs to discussion HTML for each unique shortcut
    shortcut_to_id = {}
    for idx, shortcut in enumerate(set(all_shortcuts)):
        highlight_id = f"highlight-{idx}"
        shortcut_to_id[shortcut] = highlight_id
        
        # Find the first occurrence of this shortcut in the discussion
        # Search in text nodes
        found = False
        for text_node in discussion_soup.find_all(string=re.compile(re.escape(shortcut), re.IGNORECASE)):
            if found:
                break
            
            # Get the exact match with original case
            text = str(text_node)
            pattern = re.compile(f'({re.escape(shortcut)})', re.IGNORECASE)
            match = pattern.search(text)
            
            if match:
                matched_text = match.group(1)
                # Create a span with the highlight ID
                new_html = pattern.sub(
                    f'<span id="{highlight_id}" class="policy-mention">\\1</span>',
                    text,
                    count=1
                )
                # Replace the text node
                new_soup = BeautifulSoup(new_html, 'html.parser')
                text_node.replace_with(new_soup)
                found = True
                break
    
    # Now add data-highlight attributes to the LLM output links
    def add_data_highlight(soup, shortcut_to_id):
        for link in soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
            link_text = link.get_text()
            match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
            if match:
                shortcut = match.group(1)
                if shortcut in shortcut_to_id:
                    # Add data-highlight attribute
                    link['data-highlight'] = shortcut_to_id[shortcut]
                    link['style'] = 'cursor: pointer;'
    
    add_data_highlight(policies_soup, shortcut_to_id)
    add_data_highlight(guidelines_soup, shortcut_to_id)
    add_data_highlight(essays_soup, shortcut_to_id)
    
    return (
        str(policies_soup),
        str(guidelines_soup),
        str(essays_soup),
        str(discussion_soup)
    )

