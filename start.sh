#!/bin/bash
set -e

export PATH=/opt/venv/bin:$PATH
cd backend

if [ "$SERVICE_MODE" = "cron" ]; then
  HOUR=$(date -u +%H)
  MINUTE=$(date -u +%M)
  DOW=$(date -u +%u)  # 1=Mon, 7=Sun

  echo "=== $(date -u) - Cron tick (H=$HOUR M=$MINUTE DOW=$DOW) ==="

  # Every Sunday at the first tick after 06:00 UTC: weekly reset
  if [ "$DOW" = "7" ] && [ "$HOUR" = "06" ] && [ "$MINUTE" -lt "15" ]; then
    echo "--- Weekly reset ---"
    python manage.py reset_portfolios
    python manage.py seed_bots --reset
  fi

  # Every tick: attempt price update (command self-skips via DB cooldown if
  # a previous run finished recently — safe across separate containers)
  echo "--- Price update ---"
  python manage.py fmp_update_prices --delay 0.25

  # Every tick: leaderboard update (runs after prices, fast)
  echo "--- Leaderboard update ---"
  python manage.py update_leaderboard

  echo "=== $(date -u) - Done ==="
  exit 0
fi

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
