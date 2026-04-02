#!/bin/bash
set -e

export PATH=/opt/venv/bin:$PATH

cd backend

echo "=== $(date) - Running fmp_populate_stocks ==="
python manage.py fmp_populate_stocks
echo "=== $(date) - Done ==="
