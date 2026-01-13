#!/bin/bash

# Wikipedia Policy Analyzer - Setup Script

echo "🚀 Setting up Wikipedia Policy Analyzer..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "1. Set your OpenAI API key:"
echo "   export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the application:"
echo "   python main.py"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:5000"
echo ""

