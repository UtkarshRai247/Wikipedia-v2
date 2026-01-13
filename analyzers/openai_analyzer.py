"""
OpenAI Analysis Module

This module handles the OpenAI API calls for policy/guideline/essay identification.
"""

import os
from openai import OpenAI
from config.prompts import get_analysis_prompt, SYSTEM_PROMPT


# Global variable to store the client (lazy initialization)
_client = None



def get_openai_client():
    """
    Get or create the OpenAI client (lazy initialization).
    This ensures the API key is loaded from .env before creating the client.
    """
    global _client
    if _client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please create a .env file with your OpenAI API key."
            )
        _client = OpenAI(api_key=api_key)
    return _client


def identify_policies_with_openai(discussion_text, model="gpt-4", temperature=0.3):
    """
    Use OpenAI to identify policies, guidelines, and essays in a Wikipedia discussion.
    
    Args:
        discussion_text: The extracted discussion text to analyze
        model: OpenAI model to use (default: gpt-4)
        temperature: Temperature for generation (default: 0.3 for more focused output)
        
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
        
        for category in categories:
            print(f"Analyzing {category}...")
            
            # Get the appropriate prompt for this category
            full_prompt = get_analysis_prompt(category, discussion_text)
            
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
            results[category] = result_text
            
            print(f"  → {category}: {len(result_text)} characters")
        
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


