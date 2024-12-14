#!/bin/bash
# Ensure we're in the project directory
cd "$(dirname "$0")"

# Install Python dependencies
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear