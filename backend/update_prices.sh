#!/bin/bash
# Railway cron job: update stock prices from FMP
# Schedule this service with cron: 0 14 * * 1-5 (10:00 AM ET / 14:00 UTC, weekdays)
cd /app
python manage.py fmp_update_prices
