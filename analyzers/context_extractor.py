"""
Context Extraction for Policy Mentions

This module extracts the sentences/context around policy mentions
to show HOW they're being discussed.
"""

import re


def extract_sentence_context(text, search_term, context_level='medium'):
    """
    Extract context around mentions of a search term.
    
    Args:
        text: The full text to search in
        search_term: The term to find (e.g., "WP:NPOV" or "neutral point of view")
        context_level: 'minimal' (1 sentence), 'medium' (3 sentences), 'large' (5 sentences)
        
    Returns:
        List of context snippets, each containing the mention with surrounding text
    """
    contexts = []
    
    # Define context window size
    context_windows = {
        'minimal': 0,   # Just the sentence with the mention
        'medium': 1,    # 1 sentence before + mention + 1 after
        'large': 2      # 2 sentences before + mention + 2 after
    }
    
    window = context_windows.get(context_level, 1)
    
    # Split text into sentences (basic sentence splitting)
    sentences = split_into_sentences(text)
    
    # Find all sentences containing the search term
    for i, sentence in enumerate(sentences):
        if re.search(re.escape(search_term), sentence, re.IGNORECASE):
            # Extract context window
            start_idx = max(0, i - window)
            end_idx = min(len(sentences), i + window + 1)
            
            context_sentences = sentences[start_idx:end_idx]
            context = ' '.join(context_sentences).strip()
            
            # Highlight the search term in the context
            context_with_highlight = highlight_term(context, search_term)
            
            contexts.append({
                'context': context_with_highlight,
                'sentence_index': i,
                'raw_context': context
            })
    
    return contexts


def split_into_sentences(text):
    """
    Split text into sentences.
    
    This is a simple implementation. For better results, could use NLTK or spaCy.
    
    Args:
        text: Text to split
        
    Returns:
        List of sentences
    """
    # Replace common abbreviations to avoid false splits
    text = text.replace('Mr.', 'Mr<DOT>')
    text = text.replace('Mrs.', 'Mrs<DOT>')
    text = text.replace('Dr.', 'Dr<DOT>')
    text = text.replace('vs.', 'vs<DOT>')
    text = text.replace('e.g.', 'eg<DOT>')
    text = text.replace('i.e.', 'ie<DOT>')
    text = text.replace('etc.', 'etc<DOT>')
    
    # Split on sentence boundaries
    sentences = re.split(r'[.!?]+\s+', text)
    
    # Restore abbreviations
    sentences = [s.replace('<DOT>', '.') for s in sentences]
    
    # Clean up
    sentences = [s.strip() for s in sentences if s.strip()]
    
    return sentences


def highlight_term(text, term):
    """
    Highlight a term in text using HTML bold tags.
    
    Args:
        text: Text to search in
        term: Term to highlight
        
    Returns:
        Text with term highlighted
    """
    pattern = re.compile(re.escape(term), re.IGNORECASE)
    return pattern.sub(lambda m: f'<strong>{m.group()}</strong>', text)


def find_policy_contexts(text, policy_name, shortcut=None):
    """
    Find all contexts where a policy is mentioned.
    
    Args:
        text: Full text to search
        policy_name: Full name of the policy (e.g., "Neutral point of view")
        shortcut: Shortcut (e.g., "WP:NPOV")
        
    Returns:
        List of contexts where the policy is mentioned
    """
    all_contexts = []
    
    # Search for shortcut mentions (e.g., WP:NPOV)
    if shortcut:
        contexts = extract_sentence_context(text, shortcut, context_level='medium')
        all_contexts.extend(contexts)
    
    # Search for full name mentions
    full_name_contexts = extract_sentence_context(text, policy_name, context_level='medium')
    
    # Deduplicate (avoid showing same context twice)
    existing_raw = {c['raw_context'] for c in all_contexts}
    for context in full_name_contexts:
        if context['raw_context'] not in existing_raw:
            all_contexts.append(context)
    
    return all_contexts


def format_context_for_display(contexts, max_contexts=3):
    """
    Format contexts for HTML display.
    
    Args:
        contexts: List of context dicts
        max_contexts: Maximum number of contexts to show
        
    Returns:
        HTML string
    """
    if not contexts:
        return ""
    
    html_parts = []
    
    for i, context in enumerate(contexts[:max_contexts]):
        context_html = context['context']
        html_parts.append(f'<div class="context-snippet">{context_html}</div>')
    
    if len(contexts) > max_contexts:
        html_parts.append(f'<div class="more-contexts">... and {len(contexts) - max_contexts} more mention(s)</div>')
    
    return ''.join(html_parts)


def extract_all_policy_contexts(text, policies, guidelines, essays):
    """
    Extract contexts for all detected policies, guidelines, and essays.
    
    Args:
        text: Full discussion text
        policies: List of detected policies
        guidelines: List of detected guidelines
        essays: List of detected essays
        
    Returns:
        Dict with contexts for each item
    """
    results = {
        'policies': [],
        'guidelines': [],
        'essays': []
    }
    
    # Process policies
    for policy in policies:
        contexts = find_policy_contexts(
            text, 
            policy['name'], 
            policy.get('shortcut')
        )
        results['policies'].append({
            **policy,
            'contexts': contexts,
            'context_html': format_context_for_display(contexts)
        })
    
    # Process guidelines
    for guideline in guidelines:
        contexts = find_policy_contexts(
            text,
            guideline['name'],
            guideline.get('shortcut')
        )
        results['guidelines'].append({
            **guideline,
            'contexts': contexts,
            'context_html': format_context_for_display(contexts)
        })
    
    # Process essays
    for essay in essays:
        contexts = find_policy_contexts(
            text,
            essay['name'],
            essay.get('shortcut')
        )
        results['essays'].append({
            **essay,
            'contexts': contexts,
            'context_html': format_context_for_display(contexts)
        })
    
    return results

