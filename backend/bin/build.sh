#!/bin/bash
set -e

# Install backend deps
pip install -r requirements.txt

# Build frontend
cd ../frontend
npm install
npm run build
cd ../backend

# Collect static files
python manage.py collectstatic --no-input
