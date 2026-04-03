from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.authtoken.models import Token
from stocks.models import Stock, Portfolio, PortfolioStock
from bazaar.models import BazaarUserProfile

# Each bot: (username, description, list of stock symbols to split $50k across)
BOTS = [
    # 1. FANG stocks
    ("FANG", "FANG portfolio", ["META", "AMZN", "NFLX", "GOOGL"]),
    # 2. Auto manufacturers
    ("DasAuto", "Major auto makers", ["TSLA", "F", "GM", "TM", "STLA", "HMC"]),
    # 3. Big Pharma
    ("BigPharm", "Pharma giants", ["MRNA", "PFE", "JNJ", "ABBV", "MRK", "LLY"]),
    # 4. DJT - Trump plays
    ("DJT", "DJT all-in", ["DJT", "PHUN"]),
    # 5. Techno - major tech
    ("Techno", "Big tech leaders", ["NVDA", "MSFT", "GOOGL", "ADBE", "CRM", "ORCL", "AMD", "INTC"]),
    # 6. Magnificent 7
    ("Mag7", "Magnificent Seven", ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]),
    # 7. Oil Baron
    ("OilBaron", "Energy sector", ["XOM", "CVX", "COP", "SLB", "OXY", "HAL"]),
    # 8. Defense contractor
    ("IronDome", "Defense plays", ["LMT", "RTX", "NOC", "GD", "BA", "HII"]),
    # 9. Retail therapy
    ("MallRat", "Retail kings", ["WMT", "COST", "TGT", "HD", "LOW", "TJX"]),
    # 10. Banking on it
    ("WallSt", "Banking sector", ["JPM", "BAC", "GS", "MS", "WFC", "C"]),
    # 11. Meme lord
    ("DiamondHands", "Meme stocks", ["GME", "AMC", "PLTR", "SOFI", "HOOD", "RIVN"]),
    # 12. Chip maker
    ("SiliconBrain", "Semiconductor plays", ["NVDA", "AMD", "INTC", "TSM", "AVGO", "QCOM", "MU"]),
    # 13. Streaming wars
    ("CouchPotato", "Streaming & entertainment", ["NFLX", "DIS", "WBD", "CMCSA", "EA", "TTWO"]),
    # 14. Cloud computing
    ("CloudNine", "Cloud & SaaS", ["CRM", "NOW", "SNOW", "DDOG", "NET", "ZS"]),
    # 15. Dividend aristocrat
    ("DividendDad", "Dividend blue chips", ["KO", "PEP", "PG", "JNJ", "MCD", "O"]),
    # 16. Green energy
    ("TreeHugger", "Clean energy plays", ["NEE", "FSLR", "ENPH", "PLUG", "BE", "SEDG"]),
    # 17. Biotech gambler
    ("LabRat", "Biotech bets", ["MRNA", "REGN", "VRTX", "GILD", "AMGN", "ISRG"]),
]

STARTING_BALANCE = Decimal("50000.00")
BOT_PASSWORD = "MoqBot2026!SecurePass"


class Command(BaseCommand):
    help = "Create bot accounts with themed portfolios to seed the leaderboard"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true",
            help="Delete existing bots and recreate them",
        )

    def handle(self, *args, **options):
        bot_usernames = [b[0] for b in BOTS]

        if options["reset"]:
            deleted = User.objects.filter(username__in=bot_usernames).delete()
            self.stdout.write(f"Deleted existing bots: {deleted}")

        created_bots = 0
        skipped_bots = 0

        for username, description, symbols in BOTS:
            if User.objects.filter(username=username).exists():
                self.stdout.write(f"  {username}: already exists, skipping")
                skipped_bots += 1
                continue

            try:
                self._create_bot(username, description, symbols)
                created_bots += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  {username}: FAILED - {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created: {created_bots}, Skipped: {skipped_bots}"
        ))

    @transaction.atomic
    def _create_bot(self, username, description, symbols):
        # Create user
        user = User.objects.create_user(
            username=username,
            email=f"{username.lower()}@moq.exchange",
            password=BOT_PASSWORD,
        )
        Token.objects.create(user=user)
        BazaarUserProfile.objects.create(user=user, moqs=600)
        portfolio = Portfolio.objects.create(user=user, balance=STARTING_BALANCE)

        # Look up which stocks exist in the DB
        available_stocks = Stock.objects.filter(symbol__in=symbols)
        found_symbols = {s.symbol for s in available_stocks}
        missing = [s for s in symbols if s not in found_symbols]

        if missing:
            self.stdout.write(self.style.WARNING(
                f"  {username}: missing stocks {missing}, using available only"
            ))

        if not available_stocks:
            self.stdout.write(self.style.WARNING(
                f"  {username}: no stocks found in DB, portfolio will be cash only"
            ))
            return

        # Split $50k evenly across available stocks
        stocks_list = list(available_stocks)
        allocation_per_stock = STARTING_BALANCE / len(stocks_list)
        total_spent = Decimal("0.00")

        for stock in stocks_list:
            price = stock.current_price
            if price <= 0:
                continue

            quantity = int(allocation_per_stock / price)
            if quantity <= 0:
                quantity = 1

            cost = price * quantity
            total_spent += cost

            PortfolioStock.objects.create(
                portfolio=portfolio,
                stock=stock,
                quantity=quantity,
                purchase_price=price,
            )

        # Update balance to reflect purchases
        portfolio.balance = STARTING_BALANCE - total_spent
        portfolio.save()

        invested_pct = (total_spent / STARTING_BALANCE * 100).quantize(Decimal("0.1"))
        self.stdout.write(
            f"  {username}: {len(stocks_list)} stocks, "
            f"${total_spent:.2f} invested ({invested_pct}%), "
            f"${portfolio.balance:.2f} remaining"
        )
