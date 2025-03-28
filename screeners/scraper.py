# screeners/scraper.py

import requests
from bs4 import BeautifulSoup
from .models import Stock

def run_scraper_function():
    # Define the links for each screener type
    screener_links = {
        'intraday': 'https://www.screener.in/screens/2581557/signalx-screener/',
        'short_term': 'https://www.screener.in/screens/2581767/signalx-growth-stocks-screener/',
        'long_term': 'https://www.screener.in/screens/2582036/signalx-momentum/',
        'multibagger': 'https://www.screener.in/screens/2582036/signalx-momentum/',
        'intraday_multibagger': 'https://www.screener.in/screens/2582036/signalx-momentum/',
    }

    for screener, url in screener_links.items():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Adjust the selector based on the page structure
            rows = soup.select('table tbody tr')
            for row in rows:
                cells = row.find_all('td')
                # Assuming first cell is the stock symbol, second is the stock name, and third is CMP price
                if len(cells) >= 3:
                    symbol = cells[0].get_text(strip=True)
                    name = cells[1].get_text(strip=True)
                    cmp_text = cells[2].get_text(strip=True)
                    # Clean and convert CMP price to a float
                    cmp_value = None
                    try:
                        cmp_value = float(cmp_text.replace(',', '').replace('$', ''))
                        print(cmp_value)
                    except ValueError:
                        cmp_value = None

                    Stock.objects.update_or_create(
                        stock_symbol=symbol,
                        screener_type=screener,
                        defaults={
                            'stock_name': name,
                            'cmp_price': cmp_value,
                        },
                    )
        else:
            print(f"Failed to fetch data for {screener} from {url}")
