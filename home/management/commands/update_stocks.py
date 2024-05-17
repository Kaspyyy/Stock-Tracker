import os
from django.core.management.base import BaseCommand
import yfinance as yf
from home.models import Stock
from src import settings

class Command(BaseCommand):
    help = 'Updates stock information from Yahoo Finance'

    def handle(self, *args, **kwargs):
        # symbols = ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "TSLA", "GOOG", "BRK.B", "META", "UNH", "XOM", "LLY", "JPM", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "MRK", "ABBV", "COST", "PEP", "ADBE"]
        # symbols = ["META", "UNH", "XOM", "LLY", "JPM", "JNJ", "V", "PG", "MA", "AVGO", "HD", "CVX", "MRK", "ABBV", "COST", "PEP", "ADBE"]
        symbols = ["BRK.B"]


        for symbol in symbols:
            stock_info = yf.Ticker(symbol).info
            print(stock_info)

            # # Extract necessary information
            # if stock_info.get('longName') == None:
            #     name = stock_info.get('shortName')
            # elif stock_info.get('shortName')== None:
            #     name = symbol
            # else:
            #     name = stock_info.get('longName')
            # secDescription = stock_info.get('longBusinessSummary')
            # last_price = stock_info.get('currentPrice')
            # market_cap = stock_info.get('marketCap')
            # pe_ratio = stock_info.get('trailingPegRatio')

            # # Construct the path to the logo
            # logo_file_name = f"{symbol}.svg"  # Replace .svg with the correct file extension if different
            # logo_path = os.path.join(settings.MEDIA_ROOT, 'stock_icons', logo_file_name)

            # # Check if the file exists
            # if os.path.isfile(logo_path):
            #     # Note: You need to set only the relative path from MEDIA_ROOT
            #     logo_relative_path = os.path.join('stock_icons', logo_file_name)
            # else:
            #     logo_relative_path = None  # Or set a default logo path

            # # Create or update the Stock object
            # stock, created = Stock.objects.update_or_create(
            #     symbol=symbol,
            #     defaults={
            #         'name': name,
            #         'logo': logo_relative_path,  # Set the relative path
            #         'last_price': last_price,
            #         'market_cap': market_cap,
            #         'pe_ratio': pe_ratio,
            #     }
            # )

            # if created:
            #     print(f"Created new entry for {symbol}")
            # else:
            #     print(f"Updated entry for {symbol}")
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {symbol}'))
