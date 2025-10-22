#!/bin/bash
# Setup script for Quebec Market Trends MVP

set -e  # Exit on error

echo "==========================================================="
echo "Quebec Market Trends - Setup Script"
echo "==========================================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs data/backups
echo "✓ Directories created"
echo ""

# Copy environment file if needed
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "  .env file already exists, skipping..."
fi
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x run_collection.py run_dashboard.py
echo "✓ Scripts are now executable"
echo ""

echo "==========================================================="
echo "✓ Setup complete!"
echo "==========================================================="
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Collect initial data (5-10 minutes):"
echo "     python run_collection.py"
echo ""
echo "  3. Launch the dashboard:"
echo "     python run_dashboard.py"
echo ""
echo "For more information, see QUICKSTART.md or docs/README_MVP.md"
echo ""
