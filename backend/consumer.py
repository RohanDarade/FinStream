from flask import Flask
from kafka import KafkaConsumer
import threading
#import redis
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

broker_address = 'localhost:9092'
ticker_symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC",
                  "CMCSA", "NFLX", "CSCO", "PEP", "ABNB", "QCOM", "TMUS", "AVGO", "TXN", "CHTR",
                  "AMD", "SBUX", "AMGN", "COST", "MCD", "GILD", "BKNG", "ADP", "MDLZ", "INTU",
                  "ISRG", "ZM", "VRTX", "REGN", "ATVI", "WBA", "MU", "CSX", "ILMN", "ADI",
                  "IDXX", "DXCM", "MRNA", "KLAC", "LULU", "EBAY", "EA", "NTES", "EXC"]

consumer = KafkaConsumer(bootstrap_servers=broker_address, group_id='flask-group')

ticker_symbols_lower = [symbol.lower() for symbol in ticker_symbols]
consumer.subscribe(topics=ticker_symbols_lower)

def consume_messages():
    for message in consumer:
        price = float(message.value.decode('utf-8'))
        symbol = message.topic.upper()
        print(f"Received: {symbol}: ${price:.2f}")
        redis_client.set(symbol, price)

        # Print the data stored in Redis
        for key in ticker_symbols:
            stored_price = redis_client.get(key)
            if stored_price:
                stored_price = float(stored_price.decode('utf-8'))
                print(f"Symbol: {key}, Price: {stored_price:.2f}")

def start_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

if not app.debug or not app.testing:  # Avoid starting consumer in debug or test mode
    start_consumer()

if __name__ == '__main__':
    app.run(debug=True)




# from kafka import KafkaConsumer

# broker_address = 'localhost:9092'

# # List of ticker symbols
# ticker_symbols = [
#     "AAPL", "MSFT"
#     , "AMZN", "GOOGL", "TSLA", "FB", "NVDA", "PYPL", "ADBE", "INTC",
#     "CMCSA", "NFLX", "CSCO", "PEP", "ABNB", "QCOM", "TMUS", "AVGO", "TXN", "CHTR",
#     "AMD", "SBUX", "AMGN", "COST", "MCD", "GILD", "BKNG", "ADP", "MDLZ", "INTU",
#     "ISRG", "ZM", "VRTX", "REGN", "ATVI", "WBA", "MU", "CSX", "ILMN", "ADI",
#     "IDXX", "DXCM", "MRNA", "KLAC", "LULU", "EBAY", "EA", "NTES", "EXC"
# ]
# # Kafka consumer for receiving messages
# consumer = KafkaConsumer(bootstrap_servers=broker_address)

# # Convert ticker symbols to lowercase
# ticker_symbols_lower = [symbol.lower() for symbol in ticker_symbols]

# # Subscribe to multiple topics
# consumer.subscribe(topics=ticker_symbols_lower)
# count = 0
# # Main loop to receive and print messages
# for message in consumer:
#     # Decode message value to get the price
#     price = float(message.value.decode('utf-8'))
#     # Get the ticker symbol from the topic
#     symbol = message.topic.upper()
#     print(f"Received: {symbol}: ${price:.2f} count : {count}" )
#     count += 1

