from kafka import KafkaConsumer

broker_address = 'localhost:9092'

# List of ticker symbols
ticker_symbols = [
    "AAPL", "MSFT"
    , "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC",
    "CMCSA", "NFLX", "CSCO", "PEP", "ABNB", "QCOM", "TMUS", "AVGO", "TXN", "CHTR",
    "AMD", "SBUX", "AMGN", "COST", "MCD", "GILD", "BKNG", "ADP", "MDLZ", "INTU",
    "ISRG", "ZM", "VRTX", "REGN", "ATVI", "WBA", "MU", "CSX", "ILMN", "ADI",
    "IDXX", "DXCM", "MRNA", "KLAC", "LULU", "EBAY", "EA", "NTES", "EXC"
]
# Kafka consumer for receiving messages
consumer = KafkaConsumer(bootstrap_servers=broker_address)

# Convert ticker symbols to lowercase
ticker_symbols_lower = [symbol.lower() for symbol in ticker_symbols]

# Subscribe to multiple topics
consumer.subscribe(topics=ticker_symbols_lower)

# Main loop to receive and print messages
for message in consumer:
    # Decode message value to get the price
    price = float(message.value.decode('utf-8'))
    # Get the ticker symbol from the topic
    symbol = message.topic.upper()
    print(f"Received: {symbol}: ${price:.2f}")
