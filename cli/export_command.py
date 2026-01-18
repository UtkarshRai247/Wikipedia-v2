"""
CLI Export Command

Handles 'python main.py export --url URL' command
"""

import sys
from scrapers.wikitext_scraper import fetch_wikitext_section
from analyzers.policy_extractor import extract_wikipedia_links
from analyzers.context_extractor import extract_all_policy_contexts
from exporters.sheet_exporter import format_for_sheets


def run_export(url, output_file=None, format='tsv'):
    """
    Run export command: fetch, analyze, format, output.

    Args:
        url: Wikipedia talk page URL
        output_file: Optional file path to save output
        format: Output format ('tsv', 'csv', 'json')
    """
    try:
        # Step 1: Fetch discussion
        print(f"Fetching discussion from: {url}", file=sys.stderr)
        discussion = fetch_wikitext_section(url)

        if not discussion:
            print(f"Error: Could not fetch discussion from {url}", file=sys.stderr)
            sys.exit(1)

        # Step 2: Extract policies/guidelines/essays
        print("Analyzing policies and guidelines...", file=sys.stderr)
        extracted = extract_wikipedia_links(discussion['html'], discussion['text'])

        # Step 3: Add context information
        print("Extracting context snippets...", file=sys.stderr)
        results = extract_all_policy_contexts(
            discussion['text'],
            extracted['policies'],
            extracted['guidelines'],
            extracted['essays']
        )

        # Step 4: Format for export
        output = format_for_sheets(
            results['policies'],
            results['guidelines'],
            results['essays'],
            format=format
        )

        # Step 5: Output to file or stdout
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\nExport saved to: {output_file}", file=sys.stderr)
        else:
            # Print to stdout for copy-paste
            print("\n" + "="*60, file=sys.stderr)
            print("COPY THE OUTPUT BELOW (select and copy):", file=sys.stderr)
            print("="*60 + "\n", file=sys.stderr)
            print(output)  # This goes to stdout for easy copy

        # Print summary
        print(f"\nSummary:", file=sys.stderr)
        print(f"  Policies: {len(results['policies'])}", file=sys.stderr)
        print(f"  Guidelines: {len(results['guidelines'])}", file=sys.stderr)
        print(f"  Essays: {len(results['essays'])}", file=sys.stderr)

    except Exception as e:
        print(f"Error during export: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
