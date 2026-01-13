# Quick Start Guide

## ✅ Your Application is READY!

The **Wikipedia Policy Analyzer** is currently running at:
🌐 **http://127.0.0.1:5001**

## 🚀 How to Use

1. **Open your web browser** and go to: http://127.0.0.1:5001

2. **Paste a Wikipedia talk page URL** in the input field. For example:
   - https://en.wikipedia.org/wiki/Talk:Climate_change
   - https://en.wikipedia.org/wiki/Talk:Artificial_intelligence
   - https://en.wikipedia.org/wiki/Talk:Python_(programming_language)

3. **Click "Analyze Discussion"** and wait 5-15 seconds

4. **View the results:**
   - Left side: The full Wikipedia discussion
   - Right side: Identified policies, guidelines, and essays

## 🔑 API Key

Your OpenAI API key is already configured in the `.env` file.

## 📝 Future Usage

To run the application again in the future:

```bash
cd /Users/utkarshrai/Desktop/Wikipedia
source venv/bin/activate
python main.py
```

Then open: http://127.0.0.1:5001

## 🛑 To Stop the Server

Press `Ctrl+C` in the terminal where the server is running, or run:
```bash
pkill -f "python main.py"
```

## 💡 Tips

- The app works with ANY Wikipedia talk page
- Long discussions are automatically truncated to fit OpenAI's limits
- GPT-4 provides accurate categorization of policies vs guidelines vs essays
- Both columns are independently scrollable
- The interface is fully responsive

## 📁 Project Structure

```
Wikipedia/
├── main.py              # Flask backend
├── requirements.txt     # Dependencies
├── .env                 # Your API key (DO NOT SHARE)
├── templates/
│   └── index.html      # Frontend UI
├── static/
│   └── style.css       # Styling
└── venv/               # Virtual environment
```

## 🐛 Troubleshooting

**Port already in use?**
- Change the port in `main.py` (line 120): `app.run(debug=True, port=5002, host='127.0.0.1')`

**API key not working?**
- Check your `.env` file has: `OPENAI_API_KEY=your-actual-key`

**Dependencies issues?**
- Reinstall: `pip install --upgrade -r requirements.txt`

Enjoy analyzing Wikipedia discussions! 🎉

