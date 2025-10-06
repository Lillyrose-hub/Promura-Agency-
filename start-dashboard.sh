#!/bin/bash

# PROMURA Dashboard Startup Script
# This script starts the PROMURA dashboard with all required dependencies

echo "🚀 Starting PROMURA Dashboard..."
echo "================================="

# Change to the dashboard directory
cd /root/onlysnarf-dashboard

# Activate the virtual environment
echo "📦 Activating virtual environment..."
source dashboard_env/bin/activate

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import fastapi; import jwt; import bcrypt" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️ Missing dependencies detected. Installing..."
    pip install -r requirements.txt
fi

# Change to app directory
cd app

# Create data directories if they don't exist
echo "📁 Creating data directories..."
mkdir -p data
mkdir -p media/uploads
mkdir -p logs

# Start the server
echo "✅ Starting server on http://localhost:8000"
echo "================================="
echo "📌 Default Login Credentials:"
echo "   Username: lea"
echo "   Password: admin123"
echo "   Role: Owner (Full Access)"
echo "================================="
echo ""

# Run the main application
python3 main.py