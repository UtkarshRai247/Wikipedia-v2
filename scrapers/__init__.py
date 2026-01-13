"""
Scrapers Package

Contains various scrapers for fetching Wikipedia talk page discussions.
"""

from scrapers.wikitext_scraper import fetch_wikitext_section
from scrapers.html_scraper import scrape_wikipedia_discussion

__all__ = ['fetch_wikitext_section', 'scrape_wikipedia_discussion']

