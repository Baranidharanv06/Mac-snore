#!/bin/bash
# mac-snore setup script 😴

echo "🛏️  Setting up mac-snore..."

# Check Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install it from https://python.org"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "✅ Done! Run mac-snore with:"
echo "   python3 snore.py"
echo ""
echo "⚠️  Note: macOS will ask for Accessibility permissions on first run."
echo "   Go to System Settings → Privacy & Security → Accessibility → enable Terminal"
