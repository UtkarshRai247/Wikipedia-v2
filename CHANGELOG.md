# Changelog

## [2.0.0] - 2025-11-24 - Professional Refactor

### Major Changes
- **Complete Architecture Overhaul**: Refactored monolithic codebase into professional package structure
- **Application Factory Pattern**: Implemented Flask app factory for better testability
- **Blueprint Organization**: Routes now organized as Flask blueprints
- **Package Structure**: Created dedicated packages for app, scrapers, analyzers, and config

### New Structure
```
Wikipedia/
├── app/                    # Flask application core
├── scrapers/              # Web scraping modules  
├── analyzers/             # Analysis & extraction
├── config/                # Configuration & prompts
├── static/                # Frontend assets
└── templates/             # HTML templates
```

### Added
- `app/__init__.py` - Application factory
- `app/routes.py` - Blueprint-based routing
- `app/utils.py` - Helper functions
- Package `__init__.py` files for clean imports
- `PROJECT_ARCHITECTURE.md` - Comprehensive architecture documentation
- Enhanced README with full project documentation

### Changed
- Moved `scraper.py` → `scrapers/html_scraper.py`
- Moved `wikitext_scraper.py` → `scrapers/wikitext_scraper.py`
- Moved `policy_extractor.py` → `analyzers/policy_extractor.py`
- Moved `context_extractor.py` → `analyzers/context_extractor.py`
- Moved `analyzer.py` → `analyzers/openai_analyzer.py`
- Moved `prompts.py` → `config/prompts.py`
- Simplified `main.py` to entry point only

### Removed
- `llm_context_extractor.py` - Removed unused experimental module
- All test files - Cleaned up temporary test scripts

### Technical Improvements
- Better separation of concerns
- Easier unit testing capability
- Cleaner import structure
- More maintainable codebase
- Production-ready organization

---

## [1.5.0] - 2025-11-24 - Interactive Highlighting

### Added
- Click-to-highlight functionality for policy mentions
- Auto-scroll to policy instances in discussion
- Visual highlighting with 3-second fade
- Context snippets for each policy mention

### Fixed
- Highlighting now works correctly on click
- Scroll positioning improved with offset

---

## [1.4.0] - 2025-11-24 - Context Integration

### Added
- Context extraction for policy mentions
- Sentence-level context display in right panel
- HTML ID generation for clickable mentions

### Changed
- Policy display now includes contextual snippets
- Enhanced UI for better information density

---

## [1.3.0] - 2025-11-24 - Comprehensive Policy Detection

### Added
- Exhaustive dictionary of Wikipedia policies, guidelines, and essays
- Full-name matching (case-insensitive)
- Expanded shortcut dictionary (VERIFIABLE, 3RR, 1AM, etc.)

### Fixed
- Essays now properly detected
- Missing shortcuts added
- Category classification corrected (policies vs policys)

---

## [1.2.0] - 2025-11-24 - Wikipedia API Integration

### Added
- `wikitext_scraper.py` for Wikipedia API-based scraping
- User-Agent headers to prevent 403 errors
- Toggle between HTML and wikitext scraping modes

### Changed
- Primary scraping method now uses Wikipedia API
- More reliable section extraction

---

## [1.1.0] - 2025-11-24 - Render Deployment

### Added
- `render.yaml` for automated deployment
- Gunicorn configuration
- Production-ready setup

### Fixed
- Port binding for Render compatibility
- 502 errors resolved with correct Gunicorn binding

---

## [1.0.0] - 2025-11-24 - Initial Release

### Added
- Flask web application
- Wikipedia talk page scraping
- Policy/guideline/essay detection
- Clean web interface
- OpenAI API integration (optional)

