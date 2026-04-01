#!/bin/bash
set -e

echo "=== Deploy starting ==="
echo "PATH: $PATH"
echo "PORT: $PORT"
echo "PWD: $(pwd)"

export PATH=/opt/venv/bin:$PATH

echo "Python: $(which python)"
echo "Gunicorn: $(which gunicorn)"

cd backend

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Starting gunicorn on port ${PORT:-8000} ==="
exec gunicorn fantasy_stocks.wsgi \
  --bind "0.0.0.0:${PORT:-8000}" \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
