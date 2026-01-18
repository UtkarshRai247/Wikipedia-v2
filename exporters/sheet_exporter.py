"""
Google Sheets Export Formatter

Converts policy analysis results into tab-separated format
for easy copy-paste into Google Sheets.
"""

import csv
import io
import json


def format_for_sheets(policies, guidelines, essays, format='tsv'):
    """
    Format analysis results for Google Sheets.

    Args:
        policies: List of policy dicts with 'name', 'shortcut', 'contexts'
        guidelines: List of guideline dicts
        essays: List of essay dicts
        format: 'tsv' (tab-separated), 'csv', or 'json'

    Returns:
        String ready to copy-paste into Google Sheets
    """
    if format == 'tsv':
        return _format_tsv(policies, guidelines, essays)
    elif format == 'csv':
        return _format_csv(policies, guidelines, essays)
    elif format == 'json':
        return _format_json(policies, guidelines, essays)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'tsv', 'csv', or 'json'")


def _format_tsv(policies, guidelines, essays):
    """Tab-separated format for Google Sheets paste"""
    lines = []

    # Header row
    lines.append('\t'.join(['Category', 'Name', 'Shortcut', 'Count', 'First Context', 'URL']))

    # Policies section
    for policy in policies:
        count = len(policy.get('contexts', []))
        first_context = policy['contexts'][0]['raw_context'][:100] if count > 0 else ''
        # Escape tabs and newlines in context
        first_context = first_context.replace('\t', ' ').replace('\n', ' ').strip()
        lines.append('\t'.join([
            'Policy',
            policy['name'],
            policy.get('shortcut', ''),
            str(count),
            first_context,
            policy['url']
        ]))

    # Guidelines section
    for guideline in guidelines:
        count = len(guideline.get('contexts', []))
        first_context = guideline['contexts'][0]['raw_context'][:100] if count > 0 else ''
        # Escape tabs and newlines in context
        first_context = first_context.replace('\t', ' ').replace('\n', ' ').strip()
        lines.append('\t'.join([
            'Guideline',
            guideline['name'],
            guideline.get('shortcut', ''),
            str(count),
            first_context,
            guideline['url']
        ]))

    # Essays section
    for essay in essays:
        count = len(essay.get('contexts', []))
        first_context = essay['contexts'][0]['raw_context'][:100] if count > 0 else ''
        # Escape tabs and newlines in context
        first_context = first_context.replace('\t', ' ').replace('\n', ' ').strip()
        lines.append('\t'.join([
            'Essay',
            essay['name'],
            essay.get('shortcut', ''),
            str(count),
            first_context,
            essay['url']
        ]))

    return '\n'.join(lines)


def _format_csv(policies, guidelines, essays):
    """CSV format (comma-separated)"""
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow(['Category', 'Name', 'Shortcut', 'Count', 'First Context', 'URL'])

    # Data rows - Policies
    for policy in policies:
        count = len(policy.get('contexts', []))
        first_context = policy['contexts'][0]['raw_context'][:100] if count > 0 else ''
        first_context = first_context.replace('\n', ' ').strip()
        writer.writerow([
            'Policy',
            policy['name'],
            policy.get('shortcut', ''),
            count,
            first_context,
            policy['url']
        ])

    # Data rows - Guidelines
    for guideline in guidelines:
        count = len(guideline.get('contexts', []))
        first_context = guideline['contexts'][0]['raw_context'][:100] if count > 0 else ''
        first_context = first_context.replace('\n', ' ').strip()
        writer.writerow([
            'Guideline',
            guideline['name'],
            guideline.get('shortcut', ''),
            count,
            first_context,
            guideline['url']
        ])

    # Data rows - Essays
    for essay in essays:
        count = len(essay.get('contexts', []))
        first_context = essay['contexts'][0]['raw_context'][:100] if count > 0 else ''
        first_context = first_context.replace('\n', ' ').strip()
        writer.writerow([
            'Essay',
            essay['name'],
            essay.get('shortcut', ''),
            count,
            first_context,
            essay['url']
        ])

    return output.getvalue()


def _format_json(policies, guidelines, essays):
    """JSON format for programmatic use"""
    return json.dumps({
        'policies': policies,
        'guidelines': guidelines,
        'essays': essays
    }, indent=2)
