import requests
import time
from django.core.management.base import BaseCommand
from stocks.models import Stock

# Curated list of ~200 well-known, actively traded US stocks across sectors.
# This keeps us well within the free tier's 250 calls/day limit.
STOCK_SYMBOLS = [
    # Technology
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSM", "AVGO", "ORCL", "CRM",
    "AMD", "ADBE", "INTC", "CSCO", "TXN", "QCOM", "IBM", "NOW", "INTU", "AMAT",
    "MU", "LRCX", "ADI", "KLAC", "SNPS", "CDNS", "MRVL", "FTNT", "PANW", "CRWD",
    "NET", "DDOG", "ZS", "SHOP", "SQ", "PLTR", "SNOW", "COIN", "RBLX", "U",
    # Finance
    "JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "SCHW", "AXP", "V",
    "MA", "PYPL", "COF", "USB", "PNC", "TFC", "BK", "STT", "SPGI", "ICE",
    # Healthcare
    "UNH", "JNJ", "PFE", "ABBV", "MRK", "LLY", "TMO", "ABT", "DHR", "BMY",
    "AMGN", "GILD", "ISRG", "MDT", "SYK", "BSX", "VRTX", "REGN", "ZTS", "MRNA",
    # Consumer
    "TSLA", "NKE", "SBUX", "MCD", "HD", "LOW", "TGT", "COST", "WMT", "TJX",
    "AMZN", "BKNG", "ABNB", "CMG", "YUM", "DPZ", "LULU", "ROST", "DG", "DLTR",
    "KO", "PEP", "PG", "CL", "KMB", "EL", "MNST", "KHC", "GIS", "K",
    # Energy
    "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL",
    # Industrials
    "BA", "CAT", "HON", "UPS", "RTX", "LMT", "GE", "DE", "MMM", "FDX",
    "UNP", "NSC", "WM", "RSG", "ETN", "ITW", "EMR", "ROK", "GD", "NOC",
    # Communications
    "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS", "CHTR", "WBD", "EA", "TTWO",
    # Real Estate & Utilities
    "AMT", "PLD", "CCI", "EQIX", "SPG", "O", "NEE", "DUK", "SO", "D",
    # Materials
    "LIN", "APD", "SHW", "ECL", "DD", "NEM", "FCX", "GOLD", "NUE", "STLD",
    # Meme / Popular / High-volatility
    "GME", "AMC", "RIVN", "LCID", "SOFI", "HOOD", "MARA", "RIOT", "SMCI", "ARM",
]

# Deduplicate
STOCK_SYMBOLS = list(dict.fromkeys(STOCK_SYMBOLS))

from django.conf import settings as django_settings

FMP_BASE_URL = "https://financialmodelingprep.com/stable"


class Command(BaseCommand):
    help = "Populate stocks from FMP API (profile endpoint: name, price, industry, sector)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--apikey",
            type=str,
            default=None,
            help="FMP API key (defaults to FMP_API_KEY setting)",
        )
        parser.add_argument(
            "--symbols",
            type=str,
            default=None,
            help="Comma-separated symbols to populate (overrides built-in list)",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=0.5,
            help="Delay between API calls in seconds",
        )

    def handle(self, *args, **options):
        api_key = options["apikey"] or django_settings.FMP_API_KEY
        delay = options["delay"]

        if options["symbols"]:
            symbols = [s.strip().upper() for s in options["symbols"].split(",")]
        else:
            symbols = STOCK_SYMBOLS

        self.stdout.write(f"Populating {len(symbols)} stocks from FMP...")

        created_count = 0
        updated_count = 0
        failed_count = 0

        for i, symbol in enumerate(symbols):
            try:
                resp = requests.get(
                    f"{FMP_BASE_URL}/profile",
                    params={"symbol": symbol, "apikey": api_key},
                    timeout=10,
                )

                if resp.status_code != 200:
                    self.stdout.write(self.style.WARNING(
                        f"[{i+1}/{len(symbols)}] HTTP {resp.status_code} for {symbol}"
                    ))
                    failed_count += 1
                    continue

                data = resp.json()
                if not data or not isinstance(data, list) or len(data) == 0:
                    self.stdout.write(self.style.WARNING(
                        f"[{i+1}/{len(symbols)}] No data for {symbol}"
                    ))
                    failed_count += 1
                    continue

                info = data[0]
                price = info.get("price", 0)
                if not price or price <= 0:
                    self.stdout.write(self.style.WARNING(
                        f"[{i+1}/{len(symbols)}] No price for {symbol}, skipping"
                    ))
                    failed_count += 1
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

                self.stdout.write(
                    f"[{i+1}/{len(symbols)}] {'Created' if created else 'Updated'} "
                    f"{symbol} - {info.get('companyName', '?')} @ ${price}"
                )

            except Exception as e:
                failed_count += 1
                self.stdout.write(self.style.WARNING(
                    f"[{i+1}/{len(symbols)}] Error for {symbol}: {e}"
                ))

            time.sleep(delay)

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created: {created_count}, Updated: {updated_count}, Failed: {failed_count}"
        ))
