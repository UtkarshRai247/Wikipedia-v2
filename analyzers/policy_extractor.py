"""
Wikipedia Policy Link Extractor

This module extracts Wikipedia policy, guideline, and essay links directly from
the discussion HTML and text.
"""

import re
from bs4 import BeautifulSoup
from urllib.parse import unquote


# Comprehensive Wikipedia policy/guideline/essay database
WIKIPEDIA_ITEMS = {
    "Policy": [
        "Neutral point of view",
        "No original research",
        "Verifiability",
        "Article titles",
        "Biographies of living persons",
        "Image use policy",
        "What Wikipedia is not",
        "Block evasion",
        "Civility",
        "Clean start",
        "Consensus",
        "Dispute resolution",
        "Edit warring",
        "Editing policy",
        "Harassment",
        "No personal attacks",
        "No legal threats",
        "Ownership of content",
        "Sockpuppetry",
        "Username policy",
        "Vandalism",
        "Deletion policy",
        "Speedy deletion",
        "Proposed deletion",
        "Proposed deletion (BLP)",
        "Revision deletion",
        "Oversight"
    ],
    "Guideline": [
        "Assume good faith",
        "Conflict of interest",
        "Disruptive editing",
        "Don't bite the newcomers",
        "Don't disrupt to make a point",
        "Etiquette",
        "Gaming the system",
        "Citing sources",
        "External links",
        "Reliable sources",
        "Fringe theories",
        "Naming conventions",
        "Non-free content",
        "Offensive material",
        "Article size",
        "Be bold",
        "Understandability",
        "Categories, lists, templates",
        "Categorization",
        "Disambiguation",
        "Manual of Style",
        "Notability",
        "Deletion process"
    ],
    "Essay": [
        "What no consensus really means",
        "One against many",
        "Getting your way at Wikipedia",
        "Lob a grenade and run away",
        "Always keep context in mind when arguing claims",
        "Academic Neutrality",
        "Avoid contemporary sources",
        "A POV that draws a source.",
        "Beyond the Neutral Point of View",
        "Civil POV pushing is POV pushing",
        "CIVIL POV Pushing Strategies",
        "Gendered category criterion",
        "Yes. We are biased.",
        "Don't act neutral",
        "Don't throw your POV up to the sky",
        "Systemic bias against Transformers",
        "Neutrality and consensus",
        "Neutrality of sources",
        "Neutral = source-oriented",
        "No. We are not biased.",
        "NPOV, a detailed breakdown",
        "Asymmetric controversy",
        "Crying MEDRS!",
        "Lede bombing",
        "The big mistake",
        "Writing neutrally for Wikipedia",
        "Prefer truth",
        "Splitting the difference",
        "Reliable sources for geopolitical adversaries",
        "Media, Politics, and Peace",
        "ChristianityAndNPOV",
        "Essjay neutrality",
        "Yes, you are a nerd.",
        "When interest compromises neutrality"
    ]
}

# Common shortcuts mapping (for quick detection)
# Includes both official shortcuts and common variations people use
SHORTCUTS = {
    # Policies
    'NPOV': 'Neutral point of view',
    'NOR': 'No original research',
    'OR': 'No original research',
    'V': 'Verifiability',
    'VERIFY': 'Verifiability',
    'VERIFIABLE': 'Verifiability',
    'BLP': 'Biographies of living persons',
    'NOT': 'What Wikipedia is not',
    'NOTCENSORED': 'What Wikipedia is not',
    'CENSORED': 'What Wikipedia is not',
    'CIVIL': 'Civility',
    'CIVILITY': 'Civility',
    'CON': 'Consensus',
    'CONSENSUS': 'Consensus',
    'EW': 'Edit warring',
    'EDITWAR': 'Edit warring',
    '3RR': 'Edit warring',
    'NPA': 'No personal attacks',
    'PA': 'No personal attacks',
    'SOCK': 'Sockpuppetry',
    'SOCKPUPPET': 'Sockpuppetry',
    'VAND': 'Vandalism',
    'VANDAL': 'Vandalism',
    'VANDALISM': 'Vandalism',
    
    # Guidelines
    'AGF': 'Assume good faith',
    'FAITH': 'Assume good faith',
    'COI': 'Conflict of interest',
    'CONFLICT': 'Conflict of interest',
    'BITE': "Don't bite the newcomers",
    'POINT': "Don't disrupt to make a point",
    'GAME': 'Gaming the system',
    'GAMING': 'Gaming the system',
    'CITE': 'Citing sources',
    'CITATION': 'Citing sources',
    'EL': 'External links',
    'RS': 'Reliable sources',
    'RELIABLE': 'Reliable sources',
    'SOURCE': 'Reliable sources',
    'SOURCES': 'Reliable sources',
    'UGC': 'Reliable sources',  # WP:UGC - User-generated content (redirect to RS)
    'FRINGE': 'Fringe theories',
    'MOS': 'Manual of Style',
    'MOS:LABEL': 'Manual of Style',  # MOS:LABEL - labeling guideline
    'MOS:VAR': 'Manual of Style',  # MOS:VAR - language variant guideline
    'STYLE': 'Manual of Style',
    'N': 'Notability',
    'NOTABLE': 'Notability',
    'NOTABILITY': 'Notability',
    'UNDUE': 'Neutral point of view',  # UNDUE weight is part of NPOV
    'WEIGHT': 'Neutral point of view',
    'DUE': 'Neutral point of view',
    'BALANCE': 'Neutral point of view',  # WP:BALANCE - part of NPOV policy
    'CENSORSHIP': 'What Wikipedia is not',  # WP:CENSORSHIP - redirect to NOT
    'BRD': 'Be bold',
    'BOLD': 'Be bold',
    'DISRUPTIVE': 'Disruptive editing',
    'DISRUPT': 'Disruptive editing',
    
    # Essays (common ones)
    'IAR': 'Ignore all rules',
    'DEADLINE': 'There is no deadline',
    'COMMON': 'Common sense',
    '1AM': 'One against many',
    'GRENADE': 'Lob a grenade and run away',
    'POVPUSH': 'Civil POV pushing is POV pushing',
    'STICK': 'Always keep context in mind when arguing claims',
    'BEANS': 'Always keep context in mind when arguing claims',
    'TRUTH': 'Prefer truth',
    'SPLIT': 'Splitting the difference',
}


def extract_wikipedia_links(html_content, text_content):
    """
    Extract all Wikipedia policy/guideline/essay links from the discussion.
    
    Args:
        html_content: The HTML content of the discussion
        text_content: The plain text content of the discussion
        
    Returns:
        dict with 'policies', 'guidelines', and 'essays' keys, each containing
        a list of dicts with 'name' and 'url' keys
    """
    found_items = {
        'policies': {},
        'guidelines': {},
        'essays': {}
    }
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Method 1: Extract from Wikipedia links in HTML
    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        if 'wikipedia.org/wiki/Wikipedia:' in href or href.startswith('/wiki/Wikipedia:'):
            process_wikipedia_link(href, found_items)
    
    # Method 2: Search for shortcuts in text (WP:SOMETHING and MOS:SOMETHING)
    # WP: shortcuts (allow colons for composite shortcuts like WP:NOT#INDISCRIMINATE)
    shortcut_matches = re.findall(r'\bWP:([A-Z0-9:]+)\b', text_content, re.IGNORECASE)
    for shortcut in shortcut_matches:
        shortcut_upper = shortcut.upper()
        if shortcut_upper in SHORTCUTS:
            full_name = SHORTCUTS[shortcut_upper]
            category = find_category(full_name)
            if category:
                add_item(found_items, category, full_name, f'WP:{shortcut_upper}')

    # MOS: shortcuts (Manual of Style subsections - these don't use WP: prefix)
    mos_matches = re.findall(r'\bMOS:([A-Z0-9:]+)\b', text_content, re.IGNORECASE)
    for shortcut in mos_matches:
        shortcut_upper = 'MOS:' + shortcut.upper()
        if shortcut_upper in SHORTCUTS:
            full_name = SHORTCUTS[shortcut_upper]
            category = find_category(full_name)
            if category:
                add_item(found_items, category, full_name, shortcut_upper)
        else:
            # Fallback: treat as generic MOS guideline
            full_name = 'Manual of Style'
            category = find_category(full_name)
            if category:
                add_item(found_items, category, full_name, shortcut_upper)
    
    # Method 3: Search for full names in text (case-insensitive)
    for category, items in WIKIPEDIA_ITEMS.items():
        for item_name in items:
            # For essays, use more flexible matching since they're often paraphrased
            # For policies/guidelines, use stricter matching
            
            if category == 'Essay':
                # Split into key phrases (3+ words) and search for those
                words = item_name.split()
                if len(words) >= 3:
                    # Create flexible pattern allowing some words in between
                    key_phrase = ' '.join(words[:3])  # First 3 words
                    escaped = re.escape(key_phrase)
                    pattern = escaped.replace(r'\ ', r'\s+')
                    
                    if re.search(pattern, text_content, re.IGNORECASE):
                        add_item(found_items, 'essays', item_name)
            else:
                # Strict matching for policies and guidelines
                escaped_name = re.escape(item_name)
                pattern = r'\b' + escaped_name.replace(r'\ ', r'\s+') + r'\b'
                
                if re.search(pattern, text_content, re.IGNORECASE):
                    category_key = 'policies' if category == 'Policy' else 'guidelines'
                    add_item(found_items, category_key, item_name)
    
    # Convert dicts to lists for output
    return {
        'policies': list(found_items['policies'].values()),
        'guidelines': list(found_items['guidelines'].values()),
        'essays': list(found_items['essays'].values())
    }


def process_wikipedia_link(href, found_items):
    """Process a Wikipedia link and add it to found_items if it's a policy/guideline/essay."""
    # Extract the page name
    if '/wiki/Wikipedia:' in href:
        page_name = href.split('/wiki/Wikipedia:')[-1]
    else:
        page_name = href.replace('/wiki/Wikipedia:', '')
    
    page_name = unquote(page_name.split('#')[0])  # Remove anchor and decode
    page_name = page_name.replace('_', ' ')
    
    # Check if this page name matches any known item
    for category, items in WIKIPEDIA_ITEMS.items():
        for item_name in items:
            # Case-insensitive comparison
            if page_name.lower() == item_name.lower() or item_name.lower() in page_name.lower():
                add_item(found_items, category.lower() + 's', item_name)
                return
    
    # If not found in our database, check shortcuts
    shortcut_match = re.search(r'WP[:/]?([A-Z0-9]+)', page_name, re.IGNORECASE)
    if shortcut_match:
        shortcut = shortcut_match.group(1).upper()
        if shortcut in SHORTCUTS:
            full_name = SHORTCUTS[shortcut]
            category = find_category(full_name)
            if category:
                add_item(found_items, category, full_name, f'WP:{shortcut}')


def find_category(item_name):
    """Find which category (policies/guidelines/essays) an item belongs to."""
    for category, items in WIKIPEDIA_ITEMS.items():
        if item_name in items:
            # Return proper plural forms
            if category == 'Policy':
                return 'policies'
            elif category == 'Guideline':
                return 'guidelines'
            elif category == 'Essay':
                return 'essays'
    return None


def add_item(found_items, category, item_name, shortcut=None):
    """Add an item to found_items, avoiding duplicates."""
    if category not in found_items:
        return
    
    # Use item_name as key to avoid duplicates
    if item_name not in found_items[category]:
        # Create Wikipedia URL
        url_name = item_name.replace(' ', '_')
        url = f"https://en.wikipedia.org/wiki/Wikipedia:{url_name}"
        
        found_items[category][item_name] = {
            'name': item_name,
            'shortcut': shortcut,
            'url': url
        }


def format_policy_list_with_context(policy_list, category='policy'):
    """
    Format a list of policies/guidelines/essays with context snippets.
    Includes click handlers for scrolling to mentions in the discussion.
    
    Args:
        policy_list: List of dicts with 'name', 'shortcut', 'url', 'contexts', 'context_html' keys
        category: 'policy', 'guideline', or 'essay' (for styling)
        
    Returns:
        HTML string
    """
    if not policy_list:
        return "No items explicitly mentioned in this discussion."
    
    html_parts = []
    for idx, item in enumerate(policy_list):
        shortcut = item.get('shortcut', '')
        name = item['name']
        url = item['url']
        contexts = item.get('contexts', [])
        
        # Create the policy header (clickable to scroll/highlight)
        if shortcut:
            highlight_id = f"highlight-{idx}"
            header = (
                f'<div class="policy-item-wrapper">'
                f'<div class="policy-item" data-highlight="{highlight_id}">'
                f'<a href="{url}" target="_blank" onclick="event.stopPropagation()" class="policy-link">{shortcut}</a> '
                f'<span class="policy-name">({name})</span>'
            )
            
            # Add context count
            if contexts:
                header += f' <span class="mention-count">• {len(contexts)} mention(s)</span>'
            
            header += '</div>'
            
            # Add context snippets
            if contexts:
                header += '<div class="context-snippets">'
                for i, ctx in enumerate(contexts[:2], 1):  # Show first 2 contexts
                    snippet = ctx['context']
                    # Truncate if too long
                    if len(snippet) > 200:
                        snippet = snippet[:197] + '...'
                    header += f'<div class="context-snippet">"{snippet}"</div>'
                
                if len(contexts) > 2:
                    header += f'<div class="more-contexts">... and {len(contexts) - 2} more</div>'
                
                header += '</div>'
            
            header += '</div>'
            
            html_parts.append(header)
        else:
            # No shortcut, simple display
            display = f'<div class="policy-item-wrapper"><a href="{url}" target="_blank">{name}</a></div>'
            html_parts.append(display)
    
    return ''.join(html_parts)
