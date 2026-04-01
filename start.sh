#!/bin/bash
set -e

echo "=== moq_exchange starting ==="
echo "PORT=${PORT:-not set}"
echo "DATABASE_URL=${DATABASE_URL:+is set}"

cd /app/backend

echo "Running migrations..."
python manage.py migrate --no-input 2>&1 || echo "Migration failed but continuing..."

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn fantasy_stocks.wsgi --bind "0.0.0.0:${PORT:-8000}" --timeout 120 --access-logfile - --error-logfile -
