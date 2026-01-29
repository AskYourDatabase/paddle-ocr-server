#!/bin/bash
# One-click setup for vast.ai deployment
set -e

echo "=========================================="
echo "  PaddleOCR Server Setup"
echo "=========================================="

# Install paddlepaddle-gpu from official source (PyPI doesn't have 3.x)
echo "Installing PaddlePaddle GPU from official source..."
pip install paddlepaddle-gpu==3.2.2 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

# Install other dependencies
echo "Installing other packages..."
pip install --no-cache-dir -r requirements.txt

echo "=========================================="
echo "  Setup complete!"
echo "=========================================="
echo ""
echo "Start server with: python server.py"
echo "Server will run at: http://0.0.0.0:8000"
