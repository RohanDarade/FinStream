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
  }, []);
  const gradient = [
    "bg-gradient-to-br from-red-50 to-teal-50",
    "bg-gradient-to-br from-lime-50 to-fuchsia-100",
    "bg-gradient-to-br from-slate-50 to-blue-100",
    "bg-gradient-to-br from-orange-100 to-violet-100"
  ];
  
  return (
    <div className="App p-4">
      <h1 className="text-2xl font-bold mb-4">Stock Prices</h1>
      <div className="grid grid-cols-4 gap-4">
        {Object.entries(stockData).map(([symbol, price], index) => (
          <div
            key={symbol}
            className={`border px-4 py-6 grid grid-cols-2 rounded-md ${gradient[index % gradient.length]}`}
          >
            <p className="text-lg font-bold col-span-1">{symbol}</p>
            <p className={`mt-2 col-span-1 text-right`}>
              ${price.toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
  
}

export default App;
