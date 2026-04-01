import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from stocks.models import Stock  # Adjust this import based on your project structure
from bazaar.models import BazaarListing  # Adjust this import based on your project structure
import time
class Command(BaseCommand):
    help = 'Update stock prices using Alpha Vantage API'

    def handle(self, *args, **options):
        API_KEY = 'YFSET434840297AF'
        BASE_URL = 'https://www.alphavantage.co/query'

        # Get all unique symbols from Stock model and BazaarListing model
        stock_symbols = set(Stock.objects.values_list('symbol', flat=True))
        bazaar_symbols = set(BazaarListing.objects.values_list('symbol', flat=True))
        all_symbols = stock_symbols.union(bazaar_symbols)

        self.stdout.write(f"Updating prices for {len(all_symbols)} symbols...")
        count = 0
        for symbol in all_symbols:
            count += 1
            if count > 10:
                break
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': API_KEY
            }

            try:
                response = requests.get(BASE_URL, params=params)
                data = response.json()
                print(data)
                if 'Global Quote' in data and data['Global Quote']:
                    quote = data['Global Quote']
                    current_price = float(quote.get('05. price', 0))

                    with transaction.atomic():
                        # Update Stock model
                        Stock.objects.filter(symbol=symbol).update(
                            current_price=current_price
                        )

                else:
                    self.stdout.write(self.style.WARNING(f"No data found for {symbol}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating {symbol}: {str(e)}"))

            # Add a small delay to avoid hitting API rate limits
            time.sleep(12)  # Alpha Vantage has a limit of 5 requests per minute for free tier

        self.stdout.write(self.style.SUCCESS("Stock price update completed!"))