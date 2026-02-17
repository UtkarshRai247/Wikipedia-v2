"""
Utility Functions for the Flask Application

Helper functions for HTML processing, highlighting, etc.
"""

from bs4 import BeautifulSoup, NavigableString
import re
import html


def _get_text_segments(soup):
    """
    Walk the soup and return (element, start_offset, end_offset) for each text node
    so we can map flattened text positions back to HTML nodes.
    """
    segments = []
    current = 0
    for element in soup.descendants:
        if isinstance(element, NavigableString):
            s = str(element)
            if s:
                segments.append((element, current, current + len(s)))
                current += len(s)
    return segments


def add_sentence_spans_to_html(html_content):
    """
    Add <span id="sent-N" class="sentence"> around each sentence in the discussion HTML
    so the UI can scroll to and highlight the exact sentences that mention a policy.
    
    Extracts text from HTML in document order, detects sentence boundaries, then
    wraps each sentence in a span with a stable id.
    
    Args:
        html_content: Discussion HTML
        
    Returns:
        tuple: (modified_html, sentence_texts) where sentence_texts[i] is the
        text of sentence i (so callers can map shortcuts to sentence ids).
    """
    from analyzers.context_extractor import split_into_sentences_with_offsets
    soup = BeautifulSoup(html_content, 'html.parser')
    segments = _get_text_segments(soup)
    if not segments:
        return html_content, []
    
    flattened = ''.join(str(elem) for elem, _, _ in segments)
    flat_offsets = split_into_sentences_with_offsets(flattened)
    if not flat_offsets:
        return html_content, []
    
    sentence_texts = [so['sentence'] for so in flat_offsets]
    
    # For each segment, determine which sentence span(s) overlap and wrap
    for elem, seg_start, seg_end in segments:
        seg_text = str(elem)
        if not seg_text:
            continue
        parts = []
        for idx, so in enumerate(flat_offsets):
            s_start, s_end = so['start'], so['end']
            if s_start >= seg_end or s_end <= seg_start:
                continue
            rel_start = max(0, s_start - seg_start)
            rel_end = min(len(seg_text), s_end - seg_start)
            chunk = seg_text[rel_start:rel_end]
            parts.append((rel_start, rel_end, f'<span id="sent-{idx}" class="sentence">{html.escape(chunk)}</span>'))
        if not parts:
            continue
        parts.sort(key=lambda p: p[0])
        new_parts = []
        pos = 0
        for rel_start, rel_end, wrapped in parts:
            if rel_start > pos:
                new_parts.append(html.escape(seg_text[pos:rel_start]))
            new_parts.append(wrapped)
            pos = rel_end
        if pos < len(seg_text):
            new_parts.append(html.escape(seg_text[pos:]))
        new_soup = BeautifulSoup(''.join(new_parts), 'html.parser')
        elem.replace_with(new_soup)
    
    return str(soup), sentence_texts


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


def _shortcut_appears_in_text(shortcut, text):
    """Return True if shortcut (or its suffix after :) appears in text (case-insensitive)."""
    if not (shortcut and text):
        return False
    esc = re.escape(shortcut)
    if re.search(esc, text, re.IGNORECASE):
        return True
    # Also accept bare suffix e.g. "NPOV" for "WP:NPOV"
    if ':' in shortcut:
        suffix = shortcut.split(':', 1)[1]
        if re.search(r'\b' + re.escape(suffix) + r'\b', text, re.IGNORECASE):
            return True
    return False


def ground_llm_results_to_text(policies_html, guidelines_html, essays_html, discussion_text):
    """
    Pass 2: Ground AI results to the actual discussion text.
    Only keeps policies/guidelines/essays that actually appear in the text (reduces false positives).
    
    Returns:
        tuple: (filtered_policies_html, filtered_guidelines_html, filtered_essays_html)
    """
    text = (discussion_text or "").strip()
    grounded = set()

    def collect_grounded(html, category_suffix):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
            link_text = link.get_text()
            m = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Za-z0-9]+)', link_text)
            if m and _shortcut_appears_in_text(m.group(1), text):
                grounded.add(m.group(1))

    collect_grounded(policies_html, "policy")
    collect_grounded(guidelines_html, "guideline")
    collect_grounded(essays_html, "essay")

    def rebuild_html_grounded_only(html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
            link_text = link.get_text()
            m = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Za-z0-9]+)', link_text)
            if m and m.group(1) in grounded:
                href = link.get('href', '')
                links.append(f'<a href="{href}" target="_blank">{html.escape(link_text)}</a>')
        if not links:
            return ""
        return "<p>" + ", ".join(links) + "</p>"

    out_p = rebuild_html_grounded_only(policies_html)
    out_g = rebuild_html_grounded_only(guidelines_html)
    out_e = rebuild_html_grounded_only(essays_html)
    # If a category had content but nothing grounded, show a short message
    empty_msg = "<p class=\"empty-result\">None found in this discussion.</p>"
    return (
        out_p if out_p else (empty_msg if re.search(r'<a\s', policies_html) else policies_html),
        out_g if out_g else (empty_msg if re.search(r'<a\s', guidelines_html) else guidelines_html),
        out_e if out_e else (empty_msg if re.search(r'<a\s', essays_html) else essays_html),
    )


def add_highlighting_to_llm_results(policies_html, guidelines_html, essays_html, discussion_html):
    """
    Add highlighting and scrolling support to LLM-generated results.
    Injects sentence spans into the discussion and links each policy to the
    sentences that mention it (data-sentence-ids) for direct-to-sentence scroll/highlight.
    
    Args:
        policies_html: LLM output for policies
        guidelines_html: LLM output for guidelines  
        essays_html: LLM output for essays
        discussion_html: Original discussion HTML
        
    Returns:
        tuple: (modified_policies_html, modified_guidelines_html, modified_essays_html, modified_discussion_html)
    """
    # Add sentence spans first so we have sent-0, sent-1, ... and sentence texts for mapping
    discussion_html, sentence_texts = add_sentence_spans_to_html(discussion_html)
    discussion_soup = BeautifulSoup(discussion_html, 'html.parser')
    
    # Collect all shortcuts from all categories (only from links that remain after grounding)
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
    
    # Only consider shortcuts that appear in the discussion text (Pass 2 grounding)
    unique_shortcuts = set(all_shortcuts)
    grounded_shortcuts = {
        s for s in unique_shortcuts
        if any(re.search(re.escape(s), st, re.IGNORECASE) for st in sentence_texts)
        or (':' in s and any(re.search(r'\b' + re.escape(s.split(':', 1)[1]) + r'\b', st, re.IGNORECASE) for st in sentence_texts))
    }
    
    # Map each grounded shortcut to (highlight_id, list of sentence ids that contain it)
    shortcut_to_id = {}
    shortcut_to_sentence_ids = {}
    for idx, shortcut in enumerate(sorted(grounded_shortcuts)):
        highlight_id = f"highlight-{idx}"
        shortcut_to_id[shortcut] = highlight_id
        # Which sentences mention this shortcut?
        sentence_ids = [i for i, st in enumerate(sentence_texts) if re.search(re.escape(shortcut), st, re.IGNORECASE)]
        shortcut_to_sentence_ids[shortcut] = [f"sent-{i}" for i in sentence_ids]
        
        # Find the first occurrence of this shortcut in the discussion and wrap (legacy highlight)
        found = False
        for text_node in discussion_soup.find_all(string=re.compile(re.escape(shortcut), re.IGNORECASE)):
            if found:
                break
            text = str(text_node)
            pattern = re.compile(f'({re.escape(shortcut)})', re.IGNORECASE)
            match = pattern.search(text)
            if match:
                new_html = pattern.sub(
                    f'<span id="{highlight_id}" class="policy-mention">\\1</span>',
                    text,
                    count=1
                )
                new_soup = BeautifulSoup(new_html, 'html.parser')
                text_node.replace_with(new_soup)
                found = True
                break
    
    # Add data-highlight and data-sentence-ids only to links whose shortcut is grounded
    def add_data_highlight_and_sentences(soup, shortcut_to_id, shortcut_to_sentence_ids):
        for link in soup.find_all('a', href=re.compile(r'wikipedia\.org/wiki/Wikipedia:')):
            link_text = link.get_text()
            match = re.match(r'(WP:[A-Z0-9]+|MOS:[A-Z0-9]*)', link_text)
            if match:
                shortcut = match.group(1)
                if shortcut in shortcut_to_id:
                    link['data-highlight'] = shortcut_to_id[shortcut]
                    link['style'] = 'cursor: pointer;'
                    sent_ids = shortcut_to_sentence_ids.get(shortcut, [])
                    if sent_ids:
                        link['data-sentence-ids'] = ' '.join(sent_ids)
    
    add_data_highlight_and_sentences(policies_soup, shortcut_to_id, shortcut_to_sentence_ids)
    add_data_highlight_and_sentences(guidelines_soup, shortcut_to_id, shortcut_to_sentence_ids)
    add_data_highlight_and_sentences(essays_soup, shortcut_to_id, shortcut_to_sentence_ids)
    
    return (
        str(policies_soup),
        str(guidelines_soup),
        str(essays_soup),
        str(discussion_soup)
    )

