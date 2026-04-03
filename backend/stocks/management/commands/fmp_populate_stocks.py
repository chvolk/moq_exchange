import re
import requests
import time
from django.core.management.base import BaseCommand
from stocks.models import Stock
from django.conf import settings as django_settings

FMP_BASE_URL = "https://financialmodelingprep.com/stable"
SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
SEC_USER_AGENT = "MoqExchange admin@moq.exchange"


class Command(BaseCommand):
    help = "Populate stocks from SEC ticker list + FMP profile endpoint. Supports chunking with --offset/--limit."

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
            "--offset", type=int, default=0,
            help="Start index in the ticker list (for chunking across runs)",
        )
        parser.add_argument(
            "--limit", type=int, default=0,
            help="Max stocks to process this run (0 = all remaining)",
        )
        parser.add_argument(
            "--skip-existing", action="store_true",
            help="Skip symbols already in the DB (faster for initial bulk load)",
        )

    def handle(self, *args, **options):
        api_key = options["apikey"] or django_settings.FMP_API_KEY
        delay = options["delay"]
        offset = options["offset"]
        limit = options["limit"]
        skip_existing = options["skip_existing"]

        # Step 1: Fetch SEC ticker list (~10k US-registered companies)
        self.stdout.write("Fetching ticker list from SEC...")
        try:
            resp = requests.get(
                SEC_TICKERS_URL,
                headers={"User-Agent": SEC_USER_AGENT},
                timeout=15,
            )
            resp.raise_for_status()
            sec_data = resp.json()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch SEC tickers: {e}"))
            return

        # Extract unique tickers, filtering to standard symbols (1-5 uppercase letters)
        all_tickers = []
        seen = set()
        for entry in sec_data.values():
            ticker = entry.get("ticker", "").strip().upper()
            if ticker and ticker not in seen and re.match(r'^[A-Z]{1,5}$', ticker):
                all_tickers.append(ticker)
                seen.add(ticker)

        self.stdout.write(f"Got {len(all_tickers)} valid tickers from SEC")

        # Apply offset/limit for chunking
        chunk = all_tickers[offset:]
        if limit > 0:
            chunk = chunk[:limit]

        self.stdout.write(f"Processing chunk: offset={offset}, count={len(chunk)}")

        # Get existing symbols for skip-existing mode
        existing_symbols = set()
        if skip_existing:
            existing_symbols = set(Stock.objects.values_list("symbol", flat=True))
            self.stdout.write(f"  {len(existing_symbols)} symbols already in DB (will skip)")

        created_count = 0
        updated_count = 0
        failed_count = 0
        skipped_count = 0

        for i, symbol in enumerate(chunk):
            if skip_existing and symbol in existing_symbols:
                skipped_count += 1
                continue

            try:
                resp = requests.get(
                    f"{FMP_BASE_URL}/profile",
                    params={"symbol": symbol, "apikey": api_key},
                    timeout=10,
                )

                if resp.status_code == 429:
                    self.stdout.write(self.style.ERROR(
                        f"  Rate limited at call {i+1}! Stopping early."
                    ))
                    self.stdout.write(f"  Resume with: --offset {offset + i}")
                    break

                if resp.status_code != 200:
                    failed_count += 1
                    continue

                data = resp.json()
                if not data or not isinstance(data, list) or len(data) == 0:
                    failed_count += 1
                    continue

                info = data[0]
                price = info.get("price", 0)
                if not price or price <= 0:
                    failed_count += 1
                    continue

                if not info.get("isActivelyTrading", False):
                    skipped_count += 1
                    continue

                stock, created = Stock.objects.update_or_create(
                    symbol=symbol,
                    defaults={
                        "name": info.get("companyName", symbol),
                        "current_price": price,
                        "industry": info.get("industry") or info.get("sector") or "Unknown",
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                if (created_count + updated_count) % 50 == 0:
                    self.stdout.write(
                        f"  Progress: {i+1}/{len(chunk)} | "
                        f"Created: {created_count}, Updated: {updated_count}, "
                        f"Failed: {failed_count}, Skipped: {skipped_count}"
                    )

            except Exception as e:
                failed_count += 1
                if (i + 1) % 100 == 0:
                    self.stdout.write(self.style.WARNING(f"  Error for {symbol}: {e}"))

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created: {created_count}, Updated: {updated_count}, "
            f"Failed: {failed_count}, Skipped: {skipped_count}"
        ))
        next_offset = offset + len(chunk)
        if next_offset < len(all_tickers):
            self.stdout.write(f"Next run: --offset {next_offset}")
