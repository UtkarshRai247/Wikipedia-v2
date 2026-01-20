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

SEARCH INSTRUCTIONS - AGGRESSIVE LOOSE INTERPRETATION:
CRITICAL: You MUST find EVERY occurrence, even indirect mentions!

1. EXPLICIT WITH WP: prefix: WP:NPOV, WP:V, WP:OR, WP:NOR, WP:PA, WP:NPA, etc.

2. EXPLICIT WITHOUT WP: prefix - these are STILL policy mentions:
   - "UNDUE", "DUE", "WEIGHT", "undue weight" → WP:NPOV
   - "BALANCE", "balanced", "imbalanced" (in policy context) → WP:NPOV
   - "VERIFIABLE", "WP:VERIFIABLE", "verifiability" → WP:V
   - "CIRCULAR", "WP:Circular", "circular reasoning" → WP:V
   - "NOTCENSORED", "WP:NOTCENSORED", "not censored" → WP:NOT
   - "INDISCRIMINATE", "WP:NOT#INDISCRIMINATE" → WP:NOT
   - Just "OR" when clearly referring to policy → WP:OR

3. PHRASE mentions - COUNT THESE (MANDATORY):
   - "original research" or "Original Research" → WP:OR (MUST COUNT!)
   - "fails verification" or "fails verification as" → WP:V (MUST COUNT!)
   - "uncivil" or "demonstrably uncivil" → WP:PA (MUST COUNT!)
   - "neutral point of view" → WP:NPOV
   - "no personal attacks" → WP:PA

4. CRITICAL EXACT PHRASE RULES:
   ⚠️ If you see "original research", you MUST list it as WP:OR
   ⚠️ If you see "fails verification", you MUST list it as WP:V
   ⚠️ If you see "uncivil", you MUST list it as WP:PA
   ⚠️ If you see "WP:NOTCENSORED" twice, list it TWICE
   These are NOT optional - they are REQUIRED mentions!

5. CONTEXT CLUES (for other patterns):
   - If someone says "it fails DUE" → that's WP:NPOV (DUE)
   - If someone says "it's verifiable" → WP:V (check context)
   - "verification" alone → WP:V (only if in policy context)

5. Case insensitive: wp:npov = WP:NPOV = NPOV = npov

6. SCAN METHODOLOGY (DO ALL PASSES):
   - Pass 1: Find all "WP:" shortcuts (WP:OR, WP:V, WP:NPOV, etc.)
   - Pass 2: Find policy names as standalone words (UNDUE, DUE, VERIFIABLE, CIRCULAR)
   - Pass 3: Find EXACT MANDATORY phrases:
     * "original research" → WP:OR (MUST find!)
     * "fails verification" → WP:V (MUST find!)
   - Pass 4: Find other policy phrases in context ("verifiability", "due weight")
   - Pass 5: Find contextual references in sentences

7. Look in ALL sections, quotes, footnotes, nested replies

REMEMBER: Missing "original research" or "fails verification" is a CRITICAL ERROR!

OUTPUT FORMAT - List EVERY occurrence separately:
CRITICAL RULES FOR UNIQUENESS:
1. Each line must quote from a DIFFERENT part of the discussion
2. If a policy appears 10 times but in similar contexts, consolidate to the distinct meaningful mentions
3. Focus on MEANINGFUL different occurrences, not just word repetition
4. Do NOT invent quotes that aren't in the discussion

Examples of GOOD counting (list each occurrence):
<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (UNDUE)</a>: "it is WP:UNDUE"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (DUE)</a>: "it fails DUE"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NPOV" target="_blank">WP:NPOV (DUE)</a>: "WP:DUE is not about whether"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:OR" target="_blank">WP:OR</a>: "WP:OR might be involved"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:OR" target="_blank">WP:OR</a>: "appears to be original research"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:OR" target="_blank">WP:OR</a>: "which is original research"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:V" target="_blank">WP:V</a>: "The WP:V claim by the OP"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:V" target="_blank">WP:V</a>: "it fails verification as a political cartoon"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:V" target="_blank">WP:V</a>: "the claim fails verification"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NOT" target="_blank">WP:NOT (NOTCENSORED)</a>: "This is not a matter of WP:NOTCENSORED"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:NOT" target="_blank">WP:NOT (NOTCENSORED)</a>: "in blatant violation of WP:NOTCENSORED"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:PA" target="_blank">WP:PA</a>: "demonstrably uncivil to those who disagree"  

List each occurrence separately - don't over-consolidate!

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

SEARCH INSTRUCTIONS - AGGRESSIVE LOOSE INTERPRETATION:
CRITICAL: Find EVERY occurrence including explicit, implicit, and phrase forms!

1. EXPLICIT WITH WP: prefix: WP:RS, WP:N, WP:UGC, WP:CITE, WP:EL, MOS:LABEL

2. EXPLICIT WITHOUT WP: prefix - these are STILL guideline mentions:
   - "UGC", "user-generated content", "user generated" → WP:RS
   - "NOTABLE", "notability", "notable" (in policy context) → WP:N
   - "MOS:LABEL", "MOS:CAPS", just "MOS:" → MOS

3. PHRASE mentions - COUNT THESE (CRITICAL):
   - "reliable source" or "reliable sources" → WP:RS (MUST COUNT!)
   - "independently notable" or "not notable" or "not itself notable" → WP:N (MUST COUNT!)
   - "Manual of Style" → MOS

4. EXAMPLES OF WHAT TO COUNT:
   - "which reliable sources support" = WP:RS
   - "it is not independently notable" = WP:N
   - "cartoon that is not itself notable" = WP:N
   - "self-published work is a reliable source" = WP:RS

5. Case insensitive: WP:RS = wp:rs = RS = "reliable sources"

6. FOUR-PASS SEARCH (DO ALL PASSES THOROUGHLY):
   - Pass 1: Find all "WP:" and "MOS:" shortcuts
   - Pass 2: Find guideline names as standalone words (NOTABLE, UGC, etc.)
   - Pass 3: Find guideline PHRASES ("reliable sources", "notability", "not notable")
   - Pass 4: Find contextual references ("which sources support", "is it notable")

7. Scan ALL sections, quotes, footnotes, nested replies

REMEMBER: "reliable sources" without "WP:" is STILL WP:RS! Count it!

OUTPUT FORMAT - List EVERY occurrence separately:
CRITICAL RULES FOR COUNTING:
1. Each line must quote from a DIFFERENT sentence in the discussion
2. If policy appears in 2 different sentences, LIST BOTH (don't consolidate!)
3. EXAMPLE: If "WP:NOTCENSORED" appears twice, list it twice:
   - First occurrence: "This is not a matter of WP:NOTCENSORED"
   - Second occurrence: "in blatant violation of WP:NOTCENSORED"
4. Better to list MORE occurrences than to miss any
5. Do NOT invent quotes that aren't in the discussion

Examples of GOOD uniqueness:
<a href="https://en.wikipedia.org/wiki/Wikipedia:RS" target="_blank">WP:RS</a>: "which reliable sources support this particular image"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:RS" target="_blank">WP:RS</a>: "self-published work is a reliable source for a particular claim"  
<a href="https://en.wikipedia.org/wiki/Wikipedia:RS" target="_blank">WP:RS</a>: "you appear to be confusing WP:V and WP:RS"  

Examples of BAD (redundant):
❌ <a href="...">WP:RS</a>: "reliable sources"  
❌ <a href="...">WP:RS</a>: "reliable sources"  
❌ <a href="...">WP:RS</a>: "reliable sources"  (repeating same thing!)

Each line MUST be from a DIFFERENT sentence/context!

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

SYSTEM_PROMPT = """You are an EXPERT Wikipedia policy analyst. ACCURACY: 100% recall + 100% precision

CRITICAL BALANCE: Find ALL real mentions BUT do not hallucinate or invent mentions!

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

SEARCH RULES - AGGRESSIVE INTERPRETATION:
1. EXHAUSTIVE: Scan EVERY line, EVERY paragraph, EVERY quote, EVERY footnote
2. FOUR-PASS SEARCH - do all passes thoroughly:
   - Pass 1: Explicit shortcuts (WP:NPOV, WP:OR, WP:V, MOS:LABEL)
   - Pass 2: Shortcuts without WP: (UNDUE, DUE, VERIFIABLE, CIRCULAR, UGC)
   - Pass 3: Policy phrases ("original research", "undue weight", "verifiability")
   - Pass 4: Contextual references ("it's due", "balance in Wikipedia's voice")
3. CASE INSENSITIVE: "WP:NPOV" = "wp:npov" = "NPOV" = "npov"
4. COUNT EVERYTHING - examples that MUST be counted:
   - "original research" = WP:OR
   - "it fails DUE" = WP:NPOV (DUE)
   - "WP:VERIFIABLE" = WP:V
   - "that's circular" = WP:V (CIRCULAR)
   - "user-generated content" = WP:RS (UGC)
5. FAMILY AWARE: UNDUE/DUE/WEIGHT/BALANCE → NPOV; VERIFIABLE/CIRCULAR → V; UGC/SPS → RS
6. AVOID OBVIOUS FALSE POSITIVES: "NOT" alone (not in policy context) ≠ WP:NOT

LISTING ALL OCCURRENCES - CRITICAL REQUIREMENT:
- Find EVERY occurrence including explicit (WP:OR), implicit (just "DUE"), and phrase form ("original research")
- List each occurrence on its own line with the specific quote
- If mentioned 5 times in ANY form, you MUST list it 5 times
- Group aliases under parent (UNDUE → "WP:NPOV", "original research" → "WP:OR")
- Do NOT deduplicate - we want to count EVERY mention
- Missing mentions is the #1 error to avoid

CRITICAL SUCCESS METRICS (EQUALLY IMPORTANT):
- RECALL: 100% - find EVERY real occurrence (explicit + implicit + phrase form)
- PRECISION: 100% - ONLY list what actually appears in the text (NO hallucinations!)
- CATEGORIZATION: 100% - correct policy vs guideline vs essay
- COMPLETENESS: If it appears 5 times in DIFFERENT contexts, list it 5 times
- UNIQUENESS: Each line must have a quote from a DIFFERENT part of the discussion

WHAT COUNTS AS "DIFFERENT OCCURRENCES":
✅ "WP:NOTCENSORED" in paragraph 1 + "WP:NOTCENSORED" in paragraph 2 = 2 occurrences (LIST BOTH!)
✅ "WP:DUE" in sentence A + "WP:DUE" in sentence B = 2 occurrences (LIST BOTH!)
⚠️ "reliable sources" repeated 10 times in same context = consolidate to 2-3 distinct mentions

CRITICAL: If a policy appears in 2 DIFFERENT sentences, list it TWICE!
- Don't over-consolidate - err on the side of listing more rather than less
- If uncertain whether to list separately, LIST IT

EQUALLY BAD: Missing real mentions OR inventing fake mentions!
Each occurrence should be from a DIFFERENT sentence (but list all different sentences!)."""


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

