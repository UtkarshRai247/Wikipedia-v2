"""
OpenAI Prompts for Wikipedia Policy/Guideline/Essay Identification

This module stores all prompts used for analyzing Wikipedia discussions.
"""

POLICIES_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify ALL Wikipedia POLICIES that are DISCUSSED, MENTIONED, DEBATED, or REFERENCED.

CRITICAL INSTRUCTIONS FOR 100% ACCURACY:

1. SEARCH EXHAUSTIVELY for ALL of these patterns:
   - Shortcuts with WP: prefix (e.g., "WP:NPOV", "WP:OR", "WP:V", "WP:PA", "WP:WEIGHT")
   - Shortcuts without WP: prefix but in context (e.g., "per NPOV", "violates OR")
   - Full policy names (e.g., "Neutral Point of View", "No Original Research")
   - Wikilinks: [[WP:NPOV]], [[Wikipedia:NPOV]]
   - Lowercase/mixed case: "wp:npov", "Wp:NPOV"

2. POLICY FAMILIES - Many shortcuts are sub-policies:
   - NPOV family: WP:NPOV, WP:WEIGHT, WP:UNDUE, WP:BALANCE, WP:IMPARTIAL
   - V (Verifiability) family: WP:V, WP:CIRCULAR, WP:VERIFY
   - NOT family: WP:NOT, WP:NOTCENSORED, WP:INDISCRIMINATE, WP:NOTGUIDE
   - OR family: WP:OR, WP:NOR, WP:SYNTHESIS
   - Behavioral: WP:PA, WP:NPA, WP:CIVIL, WP:AGF, WP:3RR

3. SCAN EVERY SECTION THOROUGHLY:
   - Check each paragraph
   - Look in quotes and citations
   - Check image captions and footnotes
   - Search in nested discussion threads

4. AVOID FALSE POSITIVES:
   - ONLY count if it has "WP:" prefix OR is clearly used as a policy shortcut
   - Do NOT count: standalone words like "NOT", "IMAGE", "CENSORSHIP" without context
   - Do NOT count: "RFC", "RfC" unless it's a policy reference

5. OUTPUT FORMAT:
   For each policy found, output:
   <a href="https://en.wikipedia.org/wiki/Wikipedia:PolicyName" target="_blank">WP:SHORTCUT</a>: Brief quote showing usage

If NO policies found: "No policies explicitly mentioned in this discussion."
"""

GUIDELINES_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify ALL Wikipedia GUIDELINES that are DISCUSSED, MENTIONED, or REFERENCED.

CRITICAL INSTRUCTIONS FOR 100% ACCURACY:

1. SEARCH EXHAUSTIVELY for ALL of these patterns:
   - Shortcuts with WP: prefix (e.g., "WP:N", "WP:RS", "WP:UGC")
   - Manual of Style shortcuts: "MOS:LABEL", "MOS:CAPS", "MOS:BOLD" (note: MOS not WP!)
   - Full guideline names (e.g., "Notability", "Reliable Sources")
   - Wikilinks: [[WP:RS]], [[Wikipedia:Notability]]
   - Lowercase/mixed case: "wp:rs", "Wp:N"

2. GUIDELINE FAMILIES - Many shortcuts are sub-guidelines:
   - RS (Reliable Sources) family: WP:RS, WP:UGC, WP:SPS, WP:NEWSORG
   - Notability family: WP:N, WP:GNG, WP:NBOOK, WP:NMUSIC
   - MOS (Manual of Style) family: MOS:LABEL, MOS:CAPS, MOS:BOLD, MOS:LINK
   - Content guidelines: WP:CITE, WP:EL, WP:CAT

3. SPECIAL ATTENTION:
   - MOS shortcuts use "MOS:" NOT "WP:" (e.g., MOS:LABEL not WP:LABEL)
   - Check for "Manual of Style" spelled out
   - Look for style/formatting discussions that reference MOS

4. SCAN EVERY SECTION THOROUGHLY:
   - Check each paragraph
   - Look in quotes and citations  
   - Check image captions and footnotes
   - Search in nested discussion threads

5. AVOID FALSE POSITIVES:
   - ONLY count if it has "WP:" or "MOS:" prefix OR is clearly used as a guideline shortcut
   - Do NOT count: standalone words without context

6. OUTPUT FORMAT:
   For each guideline found, output:
   <a href="https://en.wikipedia.org/wiki/Wikipedia:GuidelineName" target="_blank">WP:SHORTCUT</a>: Brief quote showing usage

If NO guidelines found: "No guidelines explicitly mentioned in this discussion."
"""

ESSAYS_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify ALL Wikipedia ESSAYS that are mentioned or referenced.

CRITICAL INSTRUCTIONS FOR 100% ACCURACY:

1. SEARCH EXHAUSTIVELY for ALL of these patterns:
   - Shortcuts with WP: prefix (e.g., "WP:1AM", "WP:IAR", "WP:COMMON")
   - Essay numbers: "WP:1AM" (One Against Many)
   - Full essay names (e.g., "One Against Many", "Ignore All Rules")
   - Wikilinks: [[WP:1AM]], [[Wikipedia:One Against Many]]
   - Lowercase/mixed case: "wp:1am", "Wp:IAR"

2. COMMON ESSAYS TO LOOK FOR:
   - WP:1AM (One Against Many)
   - WP:IAR (Ignore All Rules)
   - WP:DEADLINE (There Is No Deadline)
   - WP:COMMON (Common Sense)
   - WP:STICK (Stick to the Point)
   - WP:BEANS (Don't Explain How to Game the System)
   - WP:SNOW (Snowball Clause)
   - WP:RANDY (Randy in Boise)
   - WP:DNFTT (Don't Feed the Trolls)

3. SCAN EVERY SECTION THOROUGHLY:
   - Check each paragraph
   - Look in quotes and citations
   - Check image captions and footnotes
   - Search in nested discussion threads

4. AVOID FALSE POSITIVES:
   - ONLY count if it has "WP:" prefix OR is clearly used as an essay shortcut
   - Essays are opinion pages, not official policy

5. OUTPUT FORMAT:
   For each essay found, output:
   <a href="https://en.wikipedia.org/wiki/Wikipedia:EssayName" target="_blank">WP:SHORTCUT</a>: Brief quote showing usage

If NO essays found: "No essays explicitly mentioned in this discussion."
"""

SYSTEM_PROMPT = """You are an EXPERT Wikipedia policy analyst with 100% accuracy requirements.

YOUR MISSION: Find EVERY SINGLE policy/guideline/essay mention with ZERO misses.

CORE RULES:
1. EXHAUSTIVE SEARCH: Scan every single line, paragraph, quote, and footnote
2. PATTERN RECOGNITION: Look for "WP:", "MOS:", shortcuts, full names, wikilinks
3. CASE INSENSITIVE: Match "WP:NPOV", "wp:npov", "Wp:NPOV" all the same
4. FAMILY AWARENESS: Recognize sub-policies (e.g., WP:WEIGHT is part of NPOV family)
5. NO FALSE POSITIVES: Only count actual policy references with proper context
6. DEDUPLICATION: List each unique item ONCE even if mentioned multiple times
7. MULTI-SECTION: Read ALL sections systematically, don't skip any

FALSE POSITIVE PREVENTION:
- "NOT" alone ≠ WP:NOT (need "WP:" or clear policy context)
- "IMAGE" alone ≠ policy (need "WP:" prefix)
- "CENSORSHIP" alone ≠ WP:NOTCENSORED (need shortcut)
- "RFC" or "RfC" ≠ policy (it's a process, not a policy)

ACCURACY TARGET: 100% recall (find all mentions) with 100% precision (no false positives)"""


def get_analysis_prompt(category, discussion_text, max_chars=100000):
    """
    Get the full prompt for a specific category with the discussion text.
    
    Args:
        category: One of 'policies', 'guidelines', or 'essays'
        discussion_text: The extracted discussion text to analyze (can be structured with sections)
        max_chars: Maximum characters of discussion text to include (default: 100K for single-call approach)
        
    Returns:
        The complete prompt string
    """
    prompts = {
        'policies': POLICIES_PROMPT,
        'guidelines': GUIDELINES_PROMPT,
        'essays': ESSAYS_PROMPT
    }
    
    if category not in prompts:
        raise ValueError(f"Unknown category: {category}")
    
    # Truncate discussion text if too long (rarely needed with gpt-4o-mini's 128K context)
    truncated_text = discussion_text[:max_chars]
    if len(discussion_text) > max_chars:
        truncated_text += "\n\n[Text truncated due to length]"
    
    return f"{prompts[category]}\n\n=== DISCUSSION TEXT TO ANALYZE ===\n{truncated_text}"

