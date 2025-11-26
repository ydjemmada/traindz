#!/bin/bash
echo "Building project..."
python3.12 -m pip install -r requirements.txt

echo "Collecting static files..."
python3.12 backend/manage.py collectstatic --noinput --clear

echo "Build complete!"
