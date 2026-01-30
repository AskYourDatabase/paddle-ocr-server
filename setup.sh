#!/bin/bash
# One-click setup for vast.ai deployment
set -e

echo "=========================================="
echo "  PaddleOCR Server Setup"
echo "=========================================="

# Install all dependencies from PyPI
echo "Installing packages..."
pip install --no-cache-dir -r requirements.txt

echo "=========================================="
echo "  Setup complete!"
echo "=========================================="
echo ""
echo "Start server with: python server.py"
echo "Server will run at: http://0.0.0.0:8000"
