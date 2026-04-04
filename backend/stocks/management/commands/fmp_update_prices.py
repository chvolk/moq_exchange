import requests
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from stocks.models import Stock
from bazaar.models import BazaarListing
from django.conf import settings as django_settings

FMP_BASE_URL = "https://financialmodelingprep.com/stable"


class Command(BaseCommand):
    help = "Update stock prices from FMP API. Priority stocks first, then the rest."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apikey", type=str, default=None,
            help="FMP API key (defaults to FMP_API_KEY setting)",
        )
        parser.add_argument(
            "--delay", type=float, default=0.5,
            help="Delay between API calls in seconds",
        )

    def handle(self, *args, **options):
        from stocks.models import PortfolioStock
        from bazaar.models import PersistentPortfolioStock

        api_key = options["apikey"] or django_settings.FMP_API_KEY
        delay = options["delay"]

        total = Stock.objects.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No stocks in DB to update."))
            return

        bazaar_symbols = set(BazaarListing.objects.values_list("symbol", flat=True))

        # Priority: stocks in weekly/persistent portfolios or bazaar listings
        weekly_symbols = set(
            PortfolioStock.objects.values_list("stock__symbol", flat=True)
        )
        persistent_symbols = set(
            PersistentPortfolioStock.objects.values_list("stock__symbol", flat=True)
        )
        priority_symbols = list(weekly_symbols | persistent_symbols | bazaar_symbols)

        remaining = list(
            Stock.objects.exclude(symbol__in=priority_symbols)
            .order_by("last_updated")
            .values_list("symbol", flat=True)
        )

        all_symbols = priority_symbols + remaining

        self.stdout.write(
            f"  {len(priority_symbols)} priority, {len(remaining)} remaining"
        )
        est_minutes = len(all_symbols) * delay / 60
        self.stdout.write(
            f"Updating {len(all_symbols)} stocks (~{est_minutes:.0f} min at {delay}s delay)..."
        )

        updated_count = 0
        failed_count = 0

        for i, symbol in enumerate(all_symbols):
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
                    self.stdout.write(f"  Progress: {i+1}/{len(all_symbols)}")

            except Exception as e:
                failed_count += 1
                if (i + 1) % 200 == 0:
                    self.stdout.write(self.style.WARNING(
                        f"  Error for {symbol}: {e}"
                    ))

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Updated: {updated_count}, Failed: {failed_count} "
            f"({len(all_symbols)} total)"
        ))
