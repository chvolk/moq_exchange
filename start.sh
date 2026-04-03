#!/bin/bash
set -e

export PATH=/opt/venv/bin:$PATH
cd backend

case "$SERVICE_MODE" in
  prices)
    echo "=== $(date) - Running fmp_update_prices (full pass) ==="
    python manage.py fmp_update_prices --chunk-size 99999 --delay 0.25
    echo "=== $(date) - Done ==="
    exit 0
    ;;
  leaderboard)
    echo "=== $(date) - Running update_leaderboard ==="
    python manage.py update_leaderboard
    echo "=== $(date) - Done ==="
    exit 0
    ;;
  weekly-reset)
    echo "=== $(date) - Running weekly reset ==="
    python manage.py reset_portfolios
    python manage.py seed_bots --reset
    echo "=== $(date) - Done ==="
    exit 0
    ;;
  *)
    # Web server
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
