import requests
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from stocks.models import Stock
from bazaar.models import BazaarListing

from django.conf import settings as django_settings

FMP_BASE_URL = "https://financialmodelingprep.com/stable"


class Command(BaseCommand):
    help = "Update stock prices from FMP API (quote endpoint)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apikey",
            type=str,
            default=None,
            help="FMP API key (defaults to FMP_API_KEY setting)",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=0.3,
            help="Delay between API calls in seconds",
        )

    def handle(self, *args, **options):
        api_key = options["apikey"] or django_settings.FMP_API_KEY
        delay = options["delay"]

        # Get all symbols we need to update
        stock_symbols = set(Stock.objects.values_list("symbol", flat=True))
        bazaar_symbols = set(BazaarListing.objects.values_list("symbol", flat=True))
        all_symbols = list(stock_symbols.union(bazaar_symbols))

        if not all_symbols:
            self.stdout.write(self.style.WARNING("No stocks in DB to update."))
            return

        self.stdout.write(f"Updating prices for {len(all_symbols)} symbols...")

        updated_count = 0
        failed_count = 0

        for i, symbol in enumerate(all_symbols):
            try:
                resp = requests.get(
                    f"{FMP_BASE_URL}/quote",
                    params={"symbol": symbol, "apikey": api_key},
                    timeout=10,
                )

                if resp.status_code != 200:
                    self.stdout.write(self.style.WARNING(
                        f"[{i+1}/{len(all_symbols)}] HTTP {resp.status_code} for {symbol}"
                    ))
                    failed_count += 1
                    continue

                data = resp.json()
                if not data or not isinstance(data, list) or len(data) == 0:
                    self.stdout.write(self.style.WARNING(
                        f"[{i+1}/{len(all_symbols)}] No data for {symbol}"
                    ))
                    failed_count += 1
                    continue

                quote = data[0]
                price = quote.get("price", 0)

                if not price or price <= 0:
                    failed_count += 1
                    continue

                with transaction.atomic():
                    Stock.objects.filter(symbol=symbol).update(current_price=price)
                    BazaarListing.objects.filter(symbol=symbol).update(price=price)

                updated_count += 1

                if (i + 1) % 50 == 0:
                    self.stdout.write(f"  Progress: {i+1}/{len(all_symbols)}")

            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.WARNING(
                    f"[{i+1}/{len(all_symbols)}] Error for {symbol}: {e}"
                ))

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Updated: {updated_count}, Failed: {failed_count}"
        ))
