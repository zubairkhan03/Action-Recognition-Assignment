#!/bin/bash

echo "========================================"
echo "Video Action Recognition App"
echo "========================================"
echo ""

echo "Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Python is not installed or not in PATH!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi
echo ""

echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies!"
    exit 1
fi
echo ""

echo "Starting Flask application..."
echo ""
echo "The app will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
