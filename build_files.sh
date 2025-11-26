#!/bin/bash
echo "Building project..."
python3 -m pip install -r requirements.txt

echo "Collecting static files..."
python3 backend/manage.py collectstatic --noinput --clear

echo "Build complete!"
