# Wikipedia Talk Page Policy Analyzer

A professional Flask web application that analyzes Wikipedia talk page discussions and identifies mentions of Wikipedia policies, guidelines, and essays with contextual information.

## 🎯 Features

- **Precise Section Extraction**: Scrapes specific discussion sections from Wikipedia talk pages using the Wikipedia API
- **Comprehensive Policy Detection**: Identifies Wikipedia policies, guidelines, and essays through:
  - Direct Wikipedia links (e.g., `[[WP:NPOV]]`)
  - Shortcut codes (e.g., `WP:NOTCENSORED`, `WP:3RR`)
  - Full name matching (e.g., "Neutral Point of View")
- **Contextual Display**: Shows sentence-level context for each policy mention
- **Interactive Navigation**: Click any policy mention to scroll to and highlight it in the discussion
- **Clean UI**: Modern, responsive interface with organized panels

## 🏗️ Project Structure

```
Wikipedia/
├── app/                        # Flask application package
│   ├── __init__.py            # App factory
│   ├── routes.py              # HTTP endpoints
│   └── utils.py               # Helper functions
├── scrapers/                   # Web scraping modules
│   ├── __init__.py
│   ├── html_scraper.py        # HTML-based scraper (legacy)
│   └── wikitext_scraper.py    # Wikipedia API scraper (active)
├── analyzers/                  # Analysis modules
│   ├── __init__.py
│   ├── policy_extractor.py    # Policy detection & categorization
│   ├── context_extractor.py   # Context sentence extraction
│   └── openai_analyzer.py     # OpenAI integration (optional)
├── config/                     # Configuration
│   ├── __init__.py
│   └── prompts.py             # AI prompt templates
├── static/                     # Frontend assets
│   └── style.css              # Application styles
├── templates/                  # HTML templates
│   └── index.html             # Main interface
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── render.yaml                # Render deployment config
└── .env                       # Environment variables (not in repo)
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YEETlord247/WIkipedia-Policy-Scraping.git
   cd WIkipedia-Policy-Scraping
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (optional, for OpenAI features)
   ```bash
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Open in browser**
   ```
   http://localhost:5001
   ```

### Production Deployment (Render)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Professional refactor"
   git push origin main
   ```

2. **Connect to Render**
   - Create a new Web Service on [Render](https://render.com)
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` configuration

3. **Set environment variables** (in Render dashboard)
   - `OPENAI_API_KEY`: Your OpenAI API key (if using AI features)

4. **Deploy**
   - Render will automatically build and deploy your application

## 📖 Usage

1. **Navigate to the application** in your web browser

2. **Enter a Wikipedia talk page URL** with a section anchor:
   ```
   https://en.wikipedia.org/wiki/Talk:Article_Name#Section_Name
   ```

3. **Click "Analyze Discussion"**

4. **View results** in three organized panels:
   - **Left**: Full discussion content
   - **Right Top**: Detected policies with context
   - **Right Middle**: Detected guidelines with context
   - **Right Bottom**: Detected essays with context

5. **Click any policy mention** in the right panel to:
   - Auto-scroll to its location in the discussion
   - Highlight the mention for 3 seconds

## 🔧 Configuration

### Scraper Mode

In `app/routes.py`, you can toggle between scraping modes:

```python
# Use 'wikitext' for Wikipedia API (recommended)
# Use 'html' for direct HTML scraping (legacy)
SCRAPER_MODE = 'wikitext'
```

### Policy Dictionary

The comprehensive policy/guideline/essay dictionary is maintained in `analyzers/policy_extractor.py` under the `WIKIPEDIA_ITEMS` constant.

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.0
- **Web Scraping**: BeautifulSoup4, Requests, Wikipedia API
- **AI Integration**: OpenAI API (optional)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Gunicorn, Render
- **Development**: Python 3.9+

## 📦 Dependencies

See `requirements.txt` for full list. Key dependencies:

- `flask==3.0.0` - Web framework
- `beautifulsoup4==4.12.2` - HTML parsing
- `requests==2.31.0` - HTTP client
- `lxml==5.1.0` - XML/HTML processing
- `python-dotenv==1.0.0` - Environment management
- `gunicorn==21.2.0` - Production WSGI server
- `openai>=1.50.0` - AI integration (optional)

## 🤝 Contributing

This is a research prototype. Contributions, issues, and feature requests are welcome!

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 👨‍💻 Author

**Utkarsh Rai**

- GitHub: [@YEETlord247](https://github.com/YEETlord247)
- Repository: [Wikipedia-Policy-Scraping](https://github.com/YEETlord247/WIkipedia-Policy-Scraping)

## 🙏 Acknowledgments

- Wikipedia for their comprehensive API
- The Flask and Python communities
- BeautifulSoup4 for excellent HTML parsing

---

Built with ❤️ for Wikipedia research and analysis
