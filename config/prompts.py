"""
OpenAI Prompts for Wikipedia Policy/Guideline/Essay Identification

This module stores all prompts used for analyzing Wikipedia discussions.
"""

POLICIES_PROMPT = """You are analyzing a Wikipedia talk page discussion to identify Wikipedia POLICIES ONLY.

OFFICIAL WIKIPEDIA POLICIES (MANDATORY RULES) - ONLY THESE:
- WP:NPOV (Neutral Point of View) - includes WP:WEIGHT, WP:UNDUE, WP:DUE, WP:BALANCE
- WP:V (Verifiability) - includes WP:CIRCULAR, WP:VERIFY
- WP:OR / WP:NOR (No Original Research)
- WP:NOT (What Wikipedia is Not) - includes WP:NOTCENSORED, WP:INDISCRIMINATE
- WP:BLP (Biographies of Living Persons)
- WP:PA / WP:NPA (No Personal Attacks)
- WP:CIVIL (Civility)
- WP:AGF (Assume Good Faith)
- WP:CON (Consensus)
- WP:EW / WP:3RR (Edit Warring / Three Revert Rule)

CRITICAL: DO NOT INCLUDE THESE (they are NOT policies):
❌ WP:RS, WP:N, WP:UGC, WP:CITE, WP:MOS - these are GUIDELINES
❌ WP:1AM, WP:IAR, WP:COMMON - these are ESSAYS
❌ RFC, RfC, IMAGE - these are not policies at all

ALIAS RECOGNITION (these are the SAME policy):
- WP:WEIGHT = WP:UNDUE = WP:DUE = all mean NPOV's undue weight section
- WP:OR = WP:NOR = same policy
- WP:PA = WP:NPA = same policy
- WP:NOTCENSORED = WP:NOT subsection
- WP:INDISCRIMINATE = WP:NOT subsection

SEARCH INSTRUCTIONS - LOOSE INTERPRETATION:
1. EXPLICIT references: WP:NPOV, WP:V, WP:OR, WP:PA, WP:NOT, WP:CIVIL, WP:AGF, etc.
2. IMPLICIT references - catch these even without "WP:" prefix:
   - "UNDUE", "DUE", "WEIGHT", "undue weight", "due weight" → WP:NPOV
   - "BALANCE", "balanced", "imbalanced" when discussing policy/neutrality → WP:NPOV
   - "CIRCULAR", "circular reasoning" when discussing sources/verification → WP:V
   - "VERIFIABLE", "verifiability" when discussing sources → WP:V
   - "censored", "censorship" when discussing content policy → WP:NOT
3. CONTEXT MATTERS: "balance in Wikipedia's own voice" = policy reference
4. Case insensitive: wp:npov = WP:NPOV
5. THREE PASSES: 
   - Pass 1: Find explicit "WP:" shortcuts
   - Pass 2: Find standalone policy keywords (UNDUE, BALANCE, CIRCULAR, etc.)
   - Pass 3: Find policy concepts in context (e.g., "fair and balanced" in policy discussion)
6. Look in ALL sections, quotes, footnotes

OUTPUT FORMAT - List EVERY occurrence separately:
CRITICAL: If a policy appears 5 times, list it 5 times with 5 different quotes!

<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (WEIGHT/UNDUE)</a>: "Quote from 1st mention"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (WEIGHT/UNDUE)</a>: "Quote from 2nd mention"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (WEIGHT/UNDUE)</a>: "Quote from 3rd mention"  

Do NOT deduplicate - list every single occurrence!

If none found: "No policies explicitly mentioned in this discussion."
"""

GUIDELINES_PROMPT = """You are analyzing a Wikipedia talk page discussion to identify Wikipedia GUIDELINES ONLY.

OFFICIAL WIKIPEDIA GUIDELINES (BEST PRACTICES) - ONLY THESE:
- WP:RS (Reliable Sources) - includes WP:UGC, WP:SPS, WP:NEWSORG
- WP:N (Notability) - includes WP:GNG, WP:NOTABLE
- WP:CITE (Citing Sources)
- WP:EL (External Links)
- WP:MOS / MOS:* (Manual of Style) - includes MOS:LABEL, MOS:CAPS, MOS:BOLD
- WP:BRD (Bold, Revert, Discuss)
- WP:FRINGE (Fringe Theories)
- WP:COI (Conflict of Interest - guideline, not policy)

CRITICAL: DO NOT INCLUDE THESE (they are NOT guidelines):
❌ WP:NPOV, WP:V, WP:OR, WP:PA, WP:CIVIL, WP:AGF - these are POLICIES
❌ WP:UNDUE, WP:DUE, WP:WEIGHT - these are NPOV (policy), not guidelines
❌ WP:1AM, WP:IAR - these are ESSAYS
❌ IMAGE, NOTCENSORED, RFCNEUTRAL - not guidelines

ALIAS RECOGNITION:
- WP:RS = WP:UGC (User Generated Content) is a subsection
- WP:N = WP:NOTABLE = WP:GNG = same guideline
- MOS:LABEL = Manual of Style subsection (use "MOS:" prefix!)

SEARCH INSTRUCTIONS - LOOSE INTERPRETATION:
1. EXPLICIT references: WP:RS, WP:N, WP:UGC, WP:CITE, WP:EL, MOS:LABEL, etc.
2. IMPLICIT references - catch these even without "WP:" prefix:
   - "UGC", "user-generated content", "user generated" when discussing sources → WP:RS
   - "reliable source", "reliable sources" → WP:RS
   - "notable", "notability" when discussing article content → WP:N
   - "MOS", "Manual of Style", "style guidelines" → MOS
3. MOS SPECIAL HANDLING:
   - Search for "MOS:LABEL", "MOS:CAPS", "MOS:" prefix
   - Also catch "Manual of Style" or "MOS" in context
4. Case insensitive: wp:rs = WP:RS
5. THREE PASSES: 
   - Pass 1: Find explicit "WP:" and "MOS:" shortcuts
   - Pass 2: Find standalone guideline keywords (UGC, LABEL, etc.)
   - Pass 3: Find guideline concepts in context (e.g., "reliable sources" in policy discussion)
6. Scan ALL sections thoroughly

OUTPUT FORMAT - List EVERY occurrence separately:
CRITICAL: If a guideline appears 3 times, list it 3 times with 3 different quotes!

<a href="https://en.wikipedia.org/wiki/Wikipedia:RS" target="_blank">WP:RS</a>: "Quote from 1st mention"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:RS" target="_blank">WP:RS</a>: "Quote from 2nd mention"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:MOS#LABEL" target="_blank">MOS:LABEL</a>: "Quote from mention"  

Do NOT deduplicate - list every single occurrence!

If none found: "No guidelines explicitly mentioned in this discussion."
"""

ESSAYS_PROMPT = """You are analyzing a Wikipedia talk page discussion to identify Wikipedia ESSAYS ONLY.

WIKIPEDIA ESSAYS (OPINION/ADVICE PAGES) - ONLY THESE:
- WP:1AM (One Against Many)
- WP:IAR (Ignore All Rules)
- WP:DEADLINE (There Is No Deadline)
- WP:COMMON (Common Sense)
- WP:STICK (Stick to the Point)
- WP:BEANS (Don't Explain How to Game)
- WP:SNOW (Snowball Clause)
- WP:RANDY (Randy in Boise)
- WP:DNFTT (Don't Feed the Trolls)

CRITICAL: DO NOT INCLUDE THESE (they are NOT essays):
❌ WP:NPOV, WP:V, WP:OR, WP:PA, WP:CIVIL, WP:AGF, WP:NOT - these are POLICIES
❌ WP:UNDUE, WP:DUE, WP:WEIGHT, WP:BALANCE - these are NPOV (policy), not essays
❌ WP:NOTCENSORED, WP:INDISCRIMINATE - these are NOT policy, not essays
❌ WP:RS, WP:N, WP:UGC, WP:MOS, WP:CITE - these are GUIDELINES
❌ WP:VERIFIABLE - this is just "WP:V" (policy), not an essay

SEARCH INSTRUCTIONS:
1. Look ONLY for: WP:1AM, WP:IAR, WP:DEADLINE, WP:COMMON, WP:STICK, WP:BEANS, WP:SNOW
2. These are opinion/advice pages, not official rules
3. Case insensitive: wp:1am = WP:1AM
4. Scan ALL sections

OUTPUT FORMAT - List EVERY occurrence separately:
<a href="https://en.wikipedia.org/wiki/Wikipedia:1AM" target="_blank">WP:1AM</a>: "Quote from 1st mention"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:1AM" target="_blank">WP:1AM</a>: "Quote from 2nd mention"  

Do NOT deduplicate - list every single occurrence!

If none found: "No essays explicitly mentioned in this discussion."
"""

SYSTEM_PROMPT = """You are an EXPERT Wikipedia policy analyst. ACCURACY REQUIREMENT: 100%

STRICT CATEGORY ENFORCEMENT:
You will be asked to find POLICIES, GUIDELINES, or ESSAYS separately.
- Each prompt lists EXACTLY what belongs in that category
- DO NOT put policies in guidelines, or guidelines in essays, etc.
- If you see "WP:RS" when looking for POLICIES, SKIP IT (it's a guideline)
- If you see "WP:1AM" when looking for POLICIES, SKIP IT (it's an essay)

ALIAS RECOGNITION (crucial for accuracy):
- WP:WEIGHT = WP:UNDUE = WP:DUE = WP:BALANCE → report as "WP:NPOV (WEIGHT/UNDUE/BALANCE)"
- WP:CIRCULAR → report as "WP:V (CIRCULAR)"
- WP:PA = WP:NPA → report as "WP:PA"
- WP:OR = WP:NOR → report as "WP:OR"
- WP:UGC is part of WP:RS → report as "WP:RS (UGC)"
- MOS:LABEL is part of MOS → report as "MOS:LABEL"

SEARCH RULES - LOOSE INTERPRETATION:
1. EXHAUSTIVE: Scan every line, paragraph, quote, footnote
2. THREE-PASS SEARCH: 
   - Pass 1: Explicit shortcuts (WP:NPOV, MOS:LABEL)
   - Pass 2: Standalone keywords (UNDUE, BALANCE, UGC, CIRCULAR)
   - Pass 3: Contextual references ("balance in Wikipedia's voice", "reliable sources")
3. CASE INSENSITIVE: "WP:NPOV" = "wp:npov" = "Wp:NPOV" = "npov"
4. CONTEXT AWARE: Include implicit policy references
   - "per NPOV" or "violates OR" → counts
   - "fair and balanced" in policy context → counts as NPOV
   - "user-generated content" → counts as RS/UGC
   - "balance in Wikipedia's own voice" → counts as NPOV/BALANCE
5. FAMILY AWARE: "UNDUE"/"DUE"/"WEIGHT"/"BALANCE" → NPOV; "CIRCULAR" → V; "UGC" → RS
6. AVOID OBVIOUS FALSE POSITIVES: "NOT" alone in non-policy context ≠ WP:NOT

LISTING ALL OCCURRENCES:
- List EVERY occurrence separately (if mentioned 5 times, list it 5 times)
- Each mention should have its own line with the specific quote where it appears
- Group aliases under parent policy (UNDUE → list as "WP:NPOV (WEIGHT/UNDUE)")
- Do NOT deduplicate - we want to see all mentions

TARGET: 100% recall + 100% precision + correct categorization"""


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

