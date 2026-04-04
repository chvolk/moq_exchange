from django.core.management.base import BaseCommand
from stocks.models import PortfolioStock, Portfolio, PortfolioHistory


class Command(BaseCommand):
    help = 'Updates the leaderboard by recalculating user portfolios and logs historical data'

    def handle(self, *args, **options):
        portfolios = Portfolio.objects.all()

        for portfolio in portfolios:
            # Portfolio value = sum of current stock holdings only (no cash)
            stock_value = sum(
                holding.stock.current_price * holding.quantity
                for holding in PortfolioStock.objects.filter(portfolio=portfolio)
            )

            # Gain/loss = current stock value vs what was paid for them
            purchase_cost = sum(
                holding.purchase_price * holding.quantity
                for holding in PortfolioStock.objects.filter(portfolio=portfolio)
            )

            portfolio.total_value = stock_value
            portfolio.total_gain_loss = stock_value - purchase_cost
            portfolio.save()

            PortfolioHistory.objects.create(
                user=portfolio.user,
                total_value=stock_value
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated leaderboard and logged historical data'))
