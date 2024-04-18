from flask import Flask, Response
from kafka import KafkaConsumer
import threading
import redis
import time
import json
from flask_cors import CORS

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})


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

        # Send updated price to all clients
        data = {'symbol': symbol, 'price': price}
        for client in clients:
            client.put(data)

def start_consumer():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

clients = set()

@app.route('/prices')
def prices():
    def generate():
        client = Client()
        clients.add(client)
        last_data = None
        try:
            while True:
                data = {symbol.decode('utf-8').upper(): float(redis_client.get(symbol)) for symbol in redis_client.keys()}
                if data != last_data:
                    last_data = data
                    yield f"data: {json.dumps(data)}\n\n"
                time.sleep(1)  # Add 1 second delay to avoid the frontend to consume too fast
                
        except GeneratorExit:
            clients.remove(client)
    return Response(generate(), mimetype='text/event-stream')


class Client:
    def __init__(self):
        self.queue = []

    def put(self, message):
        self.queue.append(message)

    def get(self):
        if not self.queue:
            raise StopIteration
        return self.queue.pop(0)

if not app.debug or not app.testing:  # Avoid starting consumer in debug or test mode
    start_consumer()

if __name__ == '__main__':
    app.run(debug=True)
