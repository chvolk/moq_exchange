#!/bin/bash
set -e

export PATH=/opt/venv/bin:$PATH
cd backend

# If SERVICE_MODE=cron, run the price update chunk and exit
if [ "$SERVICE_MODE" = "cron" ]; then
  echo "=== $(date) - Running fmp_update_prices ==="
  python manage.py fmp_update_prices
  echo "=== $(date) - Done ==="
  exit 0
fi

# Otherwise, run the web server
echo "=== Deploy starting ==="
echo "PORT: $PORT"

python manage.py migrate --noinput

echo "=== Starting gunicorn on port ${PORT:-8000} ==="
exec gunicorn fantasy_stocks.wsgi \
  --bind "0.0.0.0:${PORT:-8000}" \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  --log-level info
