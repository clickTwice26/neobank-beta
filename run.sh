#!/bin/bash

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python3 run.py init-db

# Run the application
echo "Starting Flask application..."
echo "Access the app at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
python3 run.pyInstall dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python3 -c "from app import init_db; init_db(); print('Database initialized successfully!')"

# Run the application
echo "Starting Flask application..."
echo "Access the app at: http://localhost:6001"
echo "Press Ctrl+C to stop the server"
python3 app.py