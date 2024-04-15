import random
import time
from kafka import KafkaProducer


ticker_symbols = [
    "AAPL", "MSFT"
    #, "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC",
    # "CMCSA", "NFLX", "CSCO", "PEP", "ABNB", "QCOM", "TMUS", "AVGO", "TXN", "CHTR",
    # "AMD", "SBUX", "AMGN", "COST", "MCD", "GILD", "BKNG", "ADP", "MDLZ", "INTU",
    # "ISRG", "ZM", "VRTX", "REGN", "ATVI", "WBA", "MU", "CSX", "ILMN", "ADI",
    # "IDXX", "DXCM", "MRNA", "KLAC", "LULU", "EBAY", "EA", "NTES", "EXC"
]

# Default prices for each ticker symbol
default_prices = {symbol: round(random.uniform(50, 2000), 2) for symbol in ticker_symbols}

# Initialize prices with default prices
prices = default_prices.copy()

# Kafka broker address
broker_address = 'localhost:9092'

# Create Kafka producer for each ticker symbol
producers = {symbol: KafkaProducer(bootstrap_servers=broker_address) for symbol in ticker_symbols}

# Function to update prices
def update_prices():
    global prices
    for symbol in prices:
        prices[symbol] += random.uniform(-1, 1)
        # Ensure prices don't go below 0
        prices[symbol] = max(prices[symbol], 0)

# Main loop to update and push prices to Kafka every time they change
while True:
    update_prices()
    for symbol, price in prices.items():
        # Push the new price to the corresponding topic
        topic = symbol.lower()
        producers[symbol].send(topic, str(price).encode('utf-8'))
        print(f"Sent: {symbol}: ${price:.2f} to topic: {topic}")
    time.sleep(1)  # Sleep for 1 second
