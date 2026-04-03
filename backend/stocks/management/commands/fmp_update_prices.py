import os
import sys
import tempfile
import requests
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from stocks.models import Stock
from bazaar.models import BazaarListing
from django.conf import settings as django_settings

FMP_BASE_URL = "https://financialmodelingprep.com/stable"
LOCK_FILE = os.path.join(tempfile.gettempdir(), "fmp_update_prices.lock")


class Command(BaseCommand):
    help = "Update stock prices from FMP API. Processes a chunk each run, cycling through all stocks."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apikey", type=str, default=None,
            help="FMP API key (defaults to FMP_API_KEY setting)",
        )
        parser.add_argument(
            "--delay", type=float, default=0.5,
            help="Delay between API calls in seconds",
        )
        parser.add_argument(
            "--chunk-size", type=int, default=0,
            help="Number of stocks to update per run (0 = all)",
        )

    def handle(self, *args, **options):
        api_key = options["apikey"] or django_settings.FMP_API_KEY
        delay = options["delay"]
        chunk_size = options["chunk_size"]

        # ── Lock: prevent overlapping runs ──
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE) as f:
                    lock_pid = int(f.read().strip())
                # Check if the process is still running (Unix-only; on Railway this is Linux)
                os.kill(lock_pid, 0)
                self.stdout.write(self.style.WARNING(
                    f"Another run is still active (PID {lock_pid}). Skipping."
                ))
                return
            except (OSError, ValueError):
                # Process is gone or lock file is corrupt — stale lock, remove it
                os.remove(LOCK_FILE)

        # Write our PID to the lock file
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))

        try:
            self._run(api_key, delay, chunk_size)
        finally:
            # Always clean up the lock
            try:
                os.remove(LOCK_FILE)
            except OSError:
                pass

    def _run(self, api_key, delay, chunk_size):
        from stocks.models import PortfolioStock
        from bazaar.models import PersistentPortfolioStock

        bazaar_symbols = set(BazaarListing.objects.values_list("symbol", flat=True))
        total = Stock.objects.count()

        if total == 0:
            self.stdout.write(self.style.WARNING("No stocks in DB to update."))
            return

        # Priority: stocks held in weekly or persistent portfolios come first
        weekly_symbols = set(
            PortfolioStock.objects.values_list("stock__symbol", flat=True)
        )
        persistent_symbols = set(
            PersistentPortfolioStock.objects.values_list("stock__symbol", flat=True)
        )
        priority_symbols = list(weekly_symbols | persistent_symbols | bazaar_symbols)

        # Then the rest, oldest-updated first
        remaining = list(
            Stock.objects.exclude(symbol__in=priority_symbols)
            .order_by("last_updated")
            .values_list("symbol", flat=True)
        )

        chunk = priority_symbols + remaining
        if chunk_size > 0:
            chunk = chunk[:chunk_size]

        self.stdout.write(f"  {len(priority_symbols)} priority (portfolio/bazaar), {len(remaining)} remaining")

        est_minutes = len(chunk) * delay / 60
        self.stdout.write(
            f"Updating {len(chunk)} of {total} stocks "
            f"(~{est_minutes:.0f} min at {delay}s delay)..."
        )

        updated_count = 0
        failed_count = 0

        for i, symbol in enumerate(chunk):
            try:
                resp = requests.get(
                    f"{FMP_BASE_URL}/quote",
                    params={"symbol": symbol, "apikey": api_key},
                    timeout=10,
                )

                if resp.status_code == 429:
                    self.stdout.write(self.style.ERROR(
                        f"  Rate limited at call {i+1}! Stopping early."
                    ))
                    break

                if resp.status_code != 200:
                    failed_count += 1
                    continue

                data = resp.json()
                if not data or not isinstance(data, list) or len(data) == 0:
                    failed_count += 1
                    continue

                quote = data[0]
                price = quote.get("price", 0)

                if not price or price <= 0:
                    failed_count += 1
                    continue

                with transaction.atomic():
                    Stock.objects.filter(symbol=symbol).update(
                        current_price=price,
                        last_updated=timezone.now()
                    )
                    if symbol in bazaar_symbols:
                        BazaarListing.objects.filter(symbol=symbol).update(price=price)

                updated_count += 1

                if (i + 1) % 200 == 0:
                    self.stdout.write(f"  Progress: {i+1}/{len(chunk)}")

            except Exception as e:
                failed_count += 1
                if (i + 1) % 200 == 0:
                    self.stdout.write(self.style.WARNING(
                        f"  Error for {symbol}: {e}"
                    ))

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Updated: {updated_count}, Failed: {failed_count} "
            f"(chunk {len(chunk)}/{total})"
        ))
