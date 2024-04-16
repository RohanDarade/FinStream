import React, { useState, useEffect } from 'react';

function App() {
  const [stockData, setStockData] = useState({});

  useEffect(() => {
    const eventSource = new EventSource('http://127.0.0.1:5000/prices');
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStockData(data);
    };
    
    return () => {
      eventSource.close(); // Close the event source connection when the component unmounts
    };
  }, []); // Empty dependency array ensures that the effect runs only once

  return (
    <div className="App">
      <h1>Stock Prices</h1>
      <ul>
        {Object.entries(stockData).map(([symbol, price]) => (
          <li key={symbol}>
            {symbol}: ${price.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
