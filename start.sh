#!/bin/bash
set -e

export PATH=/opt/venv/bin:$PATH
cd backend

case "$SERVICE_MODE" in
  prices)
    echo "=== $(date -u) - Price update (full pass) ==="
    python manage.py fmp_update_prices --delay 0.25
    echo "=== $(date -u) - Done ==="
    ;;
  leaderboard)
    echo "=== $(date -u) - Leaderboard update ==="
    python manage.py update_leaderboard
    echo "=== $(date -u) - Done ==="
    ;;
  weekly-reset)
    echo "=== $(date -u) - Weekly reset ==="
    python manage.py reset_portfolios
    python manage.py seed_bots --reset
    echo "=== $(date -u) - Done ==="
    ;;
  *)
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
    ;;
esac
