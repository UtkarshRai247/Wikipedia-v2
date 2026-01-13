"""
OpenAI Prompts for Wikipedia Policy/Guideline/Essay Identification

This module stores all prompts used for analyzing Wikipedia discussions.
"""

POLICIES_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify Wikipedia POLICIES that are actually DISCUSSED, MENTIONED, DEBATED, or REFERENCED in the conversation.

IMPORTANT: Only identify policies that are ACTUALLY mentioned or discussed in the text provided. Do NOT assume or infer policies based on topic - only list what is explicitly present.

Wikipedia POLICIES (mandatory rules) include:
- Core content: NPOV (Neutral Point of View), Verifiability (V), No Original Research (NOR)
- Biographical: Biographies of Living Persons (BLP)
- Behavioral: Edit warring (3RR), Civility, No personal attacks (NPA), Assume good faith (AGF), Consensus
- Content: What Wikipedia is Not (NOT), Copyright (COPY), Conflict of interest (COI)
- Access: Accessibility, Alternative text
- Other: Paid editing, Sock puppetry, Vandalism

Common shortcuts: WP:NPOV, WP:V, WP:NOR, WP:BLP, WP:3RR, WP:CIVIL, WP:NPA, WP:AGF, WP:CON, WP:NOT, WP:COPYVIO, WP:COI

Look for:
- Explicit mentions of policy names or shortcuts (e.g., "per WP:NPOV", "violates BLP")
- Direct quotes or paraphrasing of policy language
- Discussions about policy application or interpretation
- Disputes referencing policies

Format each as: <a href="https://en.wikipedia.org/wiki/Wikipedia:PolicyName" target="_blank">Policy Name</a>: Brief quote or explanation of how it's discussed.

If NO policies are actually mentioned in the discussion, respond with EXACTLY: "No policies explicitly mentioned in this discussion."
"""

GUIDELINES_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify Wikipedia GUIDELINES that are actually DISCUSSED, MENTIONED, or REFERENCED in the conversation.

IMPORTANT: Only identify guidelines that are ACTUALLY mentioned or discussed in the text provided. Do NOT assume or infer guidelines based on topic - only list what is explicitly present.

Wikipedia GUIDELINES (best-practice recommendations) include:
- Content: Notability (N), Reliable Sources (RS), Identifying reliable sources
- Style: Manual of Style (MOS), Article titles, Lead sections, Article size
- Technical: Citing sources (CITE), External links (EL), Categories
- Layout: Accessibility (ACCESS), Section organization, Infoboxes
- Images: Image use policy, Alternative text for images (ALT)
- Behavior: Bold, revert, discuss cycle (BRD), Editing policy

Common shortcuts: WP:N, WP:RS, WP:MOS, WP:CITE, WP:EL, WP:ACCESS, WP:BRD, WP:ALT

Look for:
- Explicit mentions of guideline names or shortcuts (e.g., "per WP:RS", "according to MOS")
- Discussions about notability, reliable sources, formatting
- Accessibility concerns (mobile display, screen readers, etc.)
- Citation or sourcing discussions
- Article structure or style debates

Format each as: <a href="https://en.wikipedia.org/wiki/Wikipedia:GuidelineName" target="_blank">Guideline Name</a>: Brief quote or explanation.

If NO guidelines are actually mentioned in the discussion, respond with EXACTLY: "No guidelines explicitly mentioned in this discussion."
"""

ESSAYS_PROMPT = """You are analyzing a Wikipedia talk page discussion. Your task is to identify Wikipedia ESSAYS that are mentioned or referenced.

IMPORTANT: Only identify essays that are ACTUALLY mentioned in the text provided. Essays are opinion/advice pages written by editors - they are NOT official policy or guidelines.

Common Wikipedia ESSAYS include:
- WP:COMMON (Common sense)
- WP:IAR (Ignore all rules)  
- WP:DEADLINE (There is no deadline)
- WP:STICK (Stick to the point)
- WP:BEANS (Don't explain how to game the system)
- WP:SNOW (Snowball clause)
- WP:Randy (Randy in Boise)
- WP:DNFTT (Don't feed the trolls)

Look for:
- Explicit mentions of essay shortcuts or titles
- Links to Wikipedia essay pages
- Phrases like "as the essay says" or "per WP:ESSAY"

Format each as: <a href="https://en.wikipedia.org/wiki/Wikipedia:EssayName" target="_blank">Essay Name</a>: Brief quote or context.

If NO essays are actually mentioned in the discussion, respond with EXACTLY: "No essays explicitly mentioned in this discussion."
"""

SYSTEM_PROMPT = """You are an expert at analyzing Wikipedia talk page discussions and identifying which Wikipedia policies, guidelines, and essays are explicitly mentioned or discussed. 

You must be precise and only identify items that are actually present in the text. Do not infer or assume based on the topic being discussed. Only report what is explicitly mentioned."""


def get_analysis_prompt(category, discussion_text, max_chars=10000):
    """
    Get the full prompt for a specific category with the discussion text.
    
    Args:
        category: One of 'policies', 'guidelines', or 'essays'
        discussion_text: The extracted discussion text to analyze
        max_chars: Maximum characters of discussion text to include
        
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
    
    # Truncate discussion text if too long
    truncated_text = discussion_text[:max_chars]
    if len(discussion_text) > max_chars:
        truncated_text += "\n\n[Text truncated due to length]"
    
    return f"{prompts[category]}\n\n=== DISCUSSION TEXT TO ANALYZE ===\n{truncated_text}"

