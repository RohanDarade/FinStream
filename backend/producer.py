import random
import time

# List of ticker symbols
ticker_symbols = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC",
    "CMCSA", "NFLX", "CSCO", "PEP", "ABNB", "QCOM", "TMUS", "AVGO", "TXN", "CHTR",
    "AMD", "SBUX", "AMGN", "COST", "MCD", "GILD", "BKNG", "ADP", "MDLZ", "INTU",
    "ISRG", "ZM", "VRTX", "REGN", "ATVI", "WBA", "MU", "CSX", "ILMN", "ADI",
    "IDXX", "DXCM", "MRNA", "KLAC", "LULU", "EBAY", "EA", "NTES", "EXC"
]

# Default prices for each ticker symbol
default_prices = {symbol: round(random.uniform(50, 2000), 2) for symbol in ticker_symbols}

# Initialize prices with default prices
prices = default_prices.copy()

# Function to update prices
def update_prices():
    global prices
    for symbol in prices:
        prices[symbol] += random.uniform(-1, 1)
        # Ensure prices don't go below 0
        prices[symbol] = max(prices[symbol], 0)

# Main loop to update and print prices every second
while True:
    update_prices()
    for symbol, price in prices.items():
        print(f"{symbol}: ${price:.2f}", end=", ")
    print("\n")
    time.sleep(1)
