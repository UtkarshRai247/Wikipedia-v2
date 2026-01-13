"""
OpenAI Analysis Module

This module handles the OpenAI API calls for policy/guideline/essay identification.
"""

import os
import re
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


def chunk_text(text, max_chunk_size=3000, overlap=300):
    """
    Split text into overlapping chunks to prevent missing policy mentions at boundaries.
    
    Args:
        text: The full discussion text to chunk
        max_chunk_size: Maximum characters per chunk (default: 3000)
        overlap: Number of characters to overlap between chunks (default: 300)
        
    Returns:
        List of text chunks with overlap
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = start + max_chunk_size
        
        # If this isn't the last chunk, try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings (., !, ?) within the last 200 chars of the chunk
            search_start = max(end - 200, start)
            sentence_end = max(
                text.rfind('. ', search_start, end),
                text.rfind('! ', search_start, end),
                text.rfind('? ', search_start, end),
                text.rfind('\n\n', search_start, end)  # Also break at paragraph boundaries
            )
            
            # If we found a good break point, use it
            if sentence_end > start:
                end = sentence_end + 1
        
        # Extract the chunk
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position (with overlap)
        start = end - overlap
        
        # Prevent infinite loop
        if start >= len(text):
            break
    
    return chunks


def deduplicate_policy_mentions(chunks_results):
    """
    Deduplicate policy mentions that appear in multiple chunks.
    
    Args:
        chunks_results: List of result strings from different chunks
        
    Returns:
        Combined and deduplicated result string
    """
    if not chunks_results:
        return "No items explicitly mentioned in this discussion."
    
    # Combine all results
    all_mentions = []
    for result in chunks_results:
        if result and "No" not in result and "explicitly mentioned" not in result:
            all_mentions.append(result)
    
    if not all_mentions:
        return "No items explicitly mentioned in this discussion."
    
    # Simple deduplication: combine unique mentions
    # Extract policy links using regex to find unique policies
    seen_policies = set()
    unique_mentions = []
    
    for mention in all_mentions:
        # Extract policy names from links (e.g., "Wikipedia:NPOV")
        policy_links = re.findall(r'wikipedia\.org/wiki/(Wikipedia:[^"]+)', mention, re.IGNORECASE)
        
        for link in policy_links:
            if link not in seen_policies:
                seen_policies.add(link)
                # Find the full mention containing this policy
                for line in mention.split('\n'):
                    if link in line:
                        unique_mentions.append(line)
                        break
    
    return '\n'.join(unique_mentions) if unique_mentions else "No items explicitly mentioned in this discussion."


def identify_policies_with_openai(discussion_text, model="gpt-4", temperature=0.3, chunk_size=3000):
    """
    Use OpenAI to identify policies, guidelines, and essays in a Wikipedia discussion.
    Uses intelligent chunking to prevent hallucination and missing mentions in long texts.
    
    Args:
        discussion_text: The extracted discussion text to analyze
        model: OpenAI model to use (default: gpt-4)
        temperature: Temperature for generation (default: 0.3 for more focused output)
        chunk_size: Maximum characters per chunk (default: 3000)
        
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
        
        # Split text into chunks with overlap
        chunks = chunk_text(discussion_text, max_chunk_size=chunk_size, overlap=300)
        print(f"Split into {len(chunks)} chunks for analysis")
        
        for category in categories:
            print(f"Analyzing {category}...")
            chunk_results = []
            
            # Analyze each chunk separately
            for i, chunk in enumerate(chunks):
                print(f"  Processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
                
                # Get the appropriate prompt for this category
                full_prompt = get_analysis_prompt(category, chunk)
                
                # Call OpenAI API
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": full_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=1500
                )
                
                result_text = response.choices[0].message.content.strip()
                chunk_results.append(result_text)
            
            # Deduplicate and combine results from all chunks
            combined_result = deduplicate_policy_mentions(chunk_results)
            results[category] = combined_result
            
            print(f"  → {category}: {len(combined_result)} characters (from {len(chunks)} chunks)")
        
        print("OpenAI analysis complete!")
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


