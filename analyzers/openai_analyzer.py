"""
OpenAI Analysis Module

This module handles the OpenAI API calls for policy/guideline/essay identification.
"""

import os
import re
import gc
from openai import OpenAI
from config.prompts import get_analysis_prompt, SYSTEM_PROMPT


# Global variable to store the client (lazy initialization)
_client = None



def get_openai_client():
    """
    Get or create the OpenAI client (lazy initialization).
    This ensures the API key is loaded from .env before creating the client.
    Returns None if API key is not available.
    """
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found in environment variables.")
            return None
        _client = OpenAI(api_key=api_key)
    return _client


def create_sections(text, section_size=8000):
    """
    Split text into organized sections for LLM to process systematically.
    No overlap needed since all sections sent in single API call.
    
    Args:
        text: The full discussion text to section
        section_size: Target characters per section (default: 8000)
        
    Returns:
        List of text sections
    """
    # If text is small enough, return as single section
    if len(text) <= section_size:
        return [text]
    
    sections = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = start + section_size
        
        # If this isn't the last section, try to break at a sentence/paragraph boundary
        if end < len(text):
            # Look for good break points within the last 300 chars
            search_start = max(end - 300, start)
            break_point = max(
                text.rfind('\n\n', search_start, end),  # Paragraph boundary (best)
                text.rfind('. ', search_start, end),    # Sentence ending
                text.rfind('! ', search_start, end),
                text.rfind('? ', search_start, end)
            )
            
            # If we found a good break point, use it
            if break_point > start:
                end = break_point + 1
        
        # Extract the section
        section = text[start:end].strip()
        if section:
            sections.append(section)
        
        # Move to next section (no overlap)
        start = end
    
    return sections


def format_structured_text(sections):
    """
    Format sections with clear markers for LLM to process systematically.
    
    Args:
        sections: List of text sections
        
    Returns:
        Formatted string with section markers
    """
    if len(sections) == 1:
        return sections[0]
    
    structured_text = f"This discussion has been divided into {len(sections)} sections for clarity.\n"
    structured_text += "Please read through ALL sections systematically and identify EVERY unique mention.\n\n"
    
    for i, section in enumerate(sections, 1):
        structured_text += f"\n{'='*60}\n"
        structured_text += f"SECTION {i} OF {len(sections)}\n"
        structured_text += f"{'='*60}\n\n"
        structured_text += section
    
    return structured_text


def identify_policies_with_openai(discussion_text, model="gpt-4o", temperature=0.1, section_size=8000):
    """
    Use OpenAI to identify policies, guidelines, and essays in a Wikipedia discussion.
    Uses structured sections in a single API call per category for optimal performance.
    
    Args:
        discussion_text: The extracted discussion text to analyze
        model: OpenAI model to use (default: gpt-4o-mini)
        temperature: Temperature for generation (default: 0.3 for more focused output)
        section_size: Target characters per section (default: 8000)
        
    Returns:
        dict with 'policies', 'guidelines', and 'essays' keys containing the analysis
    """
    try:
        categories = ['policies', 'guidelines', 'essays']
        results = {}
        
        print(f"Analyzing discussion with OpenAI (model: {model})...")
        print(f"Discussion text length: {len(discussion_text)} characters")
        
        # Get the OpenAI client (lazy initialization)
        client = get_openai_client()
        
        if client is None:
            error_msg = "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
            print(f"ERROR: {error_msg}")
            return {
                'policies': f'<p class="error">{error_msg}</p>',
                'guidelines': f'<p class="error">{error_msg}</p>',
                'essays': f'<p class="error">{error_msg}</p>'
            }
        
        # Split text into organized sections (for LLM readability)
        sections = create_sections(discussion_text, section_size=section_size)
        print(f"Organized into {len(sections)} section(s) for structured analysis")
        
        # Format sections with clear markers
        structured_text = format_structured_text(sections)
        
        for category in categories:
            print(f"Analyzing {category} (single API call)...")
            
            # Get the appropriate prompt for this category with structured text
            full_prompt = get_analysis_prompt(category, structured_text)
            
            # Single API call with all sections
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=temperature,
                max_tokens=2000  # Increased from 1500 to allow more complete listings
            )
            
            result_text = response.choices[0].message.content.strip()
            results[category] = result_text
            
            # Clear from memory
            gc.collect()
            
            print(f"  ✓ {category}: {len(result_text)} characters")
        
        print(f"\n✓ Analysis complete! (3 API calls total)")
        return results
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'policies': f'Error: {str(e)}',
            'guidelines': f'Error: {str(e)}',
            'essays': f'Error: {str(e)}'
        }


def batch_analyze_discussions(discussions, model="gpt-4"):
    """
    Analyze multiple discussions in batch.
    
    Args:
        discussions: List of dicts with 'url' and 'text' keys
        model: OpenAI model to use
        
    Returns:
        List of analysis results
    """
    results = []
    
    for idx, discussion in enumerate(discussions):
        print(f"\n=== Analyzing discussion {idx + 1}/{len(discussions)} ===")
        print(f"URL: {discussion.get('url', 'Unknown')}")
        
        analysis = identify_policies_with_openai(discussion['text'], model=model)
        
        results.append({
            'url': discussion.get('url'),
            'analysis': analysis
        })
    
    return results

def batch_analyze_discussions_with_context(discussions, model="gpt-4"):
    """
    Analyze multiple discussions in batch with context.
    
    Args:
        discussions: List of dicts with 'url' and 'text' keys
        model: OpenAI model to use
        
        return results
    """
    results = []
    for idx, discussion in enumerate(discussions):
        print(f"\n=== Analyzing discussion {idx + 1}/{len(discussions)} ===")
        print(f"URL: {discussion.get('url', 'Unknown')}")
        
        analysis = identify_policies_with_openai(discussion['text'], model=model)
        
        results.append({
            'url': discussion.get('url'),
            'analysis': analysis
        })
    return results


