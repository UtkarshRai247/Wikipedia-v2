# Project Architecture

## Overview

This is a professional Flask application with a modular, scalable architecture following best practices for Python web applications.

## Architecture Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Package Structure**: Organized into logical packages (app, scrapers, analyzers, config)
3. **Application Factory Pattern**: Flask app is created via factory function for better testing and configuration
4. **Blueprint Pattern**: Routes are organized in blueprints for modularity
5. **Dependency Injection**: Components are loosely coupled through clean interfaces

## Package Details

### `app/` - Flask Application Core
- **`__init__.py`**: Application factory (`create_app()`)
- **`routes.py`**: HTTP endpoints organized as Blueprint
- **`utils.py`**: Helper functions for HTML processing and highlighting

### `scrapers/` - Data Collection
- **`__init__.py`**: Package exports
- **`html_scraper.py`**: Direct HTML scraping (legacy fallback)
- **`wikitext_scraper.py`**: Wikipedia API integration (primary method)

### `analyzers/` - Content Analysis
- **`__init__.py`**: Package exports
- **`policy_extractor.py`**: Policy/guideline/essay detection with comprehensive dictionary
- **`context_extractor.py`**: Sentence-level context extraction
- **`openai_analyzer.py`**: Optional AI-powered analysis

### `config/` - Configuration Management
- **`__init__.py`**: Package exports
- **`prompts.py`**: AI prompt templates and system messages

## Data Flow

```
User Request
    ↓
app/routes.py (Blueprint endpoint)
    ↓
scrapers/wikitext_scraper.py (Fetch discussion)
    ↓
analyzers/policy_extractor.py (Extract policies)
    ↓
analyzers/context_extractor.py (Extract contexts)
    ↓
app/utils.py (Add highlight IDs)
    ↓
JSON Response → Frontend
```

## Design Patterns Used

1. **Factory Pattern**: `create_app()` for Flask initialization
2. **Blueprint Pattern**: Route organization
3. **Module Pattern**: Each package is self-contained
4. **Strategy Pattern**: Multiple scraper implementations (HTML vs API)
5. **Lazy Initialization**: OpenAI client loaded on-demand

## Testing Strategy

Each module can be tested independently:

```python
# Test scrapers
from scrapers import fetch_wikitext_section
result = fetch_wikitext_section(url)

# Test analyzers
from analyzers import extract_wikipedia_links
policies = extract_wikipedia_links(html, text)

# Test utilities
from app.utils import add_highlight_ids
html_with_ids = add_highlight_ids(html, items)
```

## Deployment Considerations

- **Development**: Uses Flask built-in server (`python main.py`)
- **Production**: Uses Gunicorn WSGI server (configured in `render.yaml`)
- **Environment Variables**: Loaded via python-dotenv
- **Static Files**: Served via Flask in dev, reverse proxy in production
- **Error Handling**: Comprehensive try-catch with logging

## Future Enhancements

- [ ] Add comprehensive unit tests
- [ ] Implement caching layer (Redis)
- [ ] Add database for analytics
- [ ] Create API rate limiting
- [ ] Add user authentication
- [ ] Implement background job queue for large analyses

## Code Quality Standards

- **PEP 8**: Python style guide compliance
- **Docstrings**: All functions documented
- **Type Hints**: Consider adding for better IDE support
- **Error Handling**: Graceful degradation
- **Logging**: Structured logging for debugging

