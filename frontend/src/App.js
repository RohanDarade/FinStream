import React, { useState, useEffect } from 'react';

function App() {
  const [stockData, setStockData] = useState({});

  useEffect(() => {
    const eventSource = new EventSource('http://127.0.0.1:5000/prices');
    let intervalId; // Declare the interval ID

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStockData(data);
    };

    // Set up the interval after the initial connection
    eventSource.onopen = () => {
      intervalId = setInterval(() => {
        // Close the previous connection and create a new one
        eventSource.close();
        const newEventSource = new EventSource('http://127.0.0.1:5000/prices');
        newEventSource.onmessage = (event) => {
          const newData = JSON.parse(event.data);
          setStockData(newData);
        };
      }, 1000);
    };

    return () => {
      clearInterval(intervalId); // Clear the interval when the component unmounts
      eventSource.close(); // Close the event source connection
    };
  }, []);

  return (
    <div className="App">
      <h1 className="text-2xl font-bold mb-4">Stock Prices</h1>
      <div className="grid grid-cols-2 gap-4">
        {Object.entries(stockData).map(([symbol, price]) => (
          <div key={symbol} className="border p-4">
            <p className="text-lg font-bold">{symbol}</p>
            <p className="mt-2">${price.toFixed(2)}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;


// import React, { useState, useEffect } from 'react';

// function App() {
//   const [stockData, setStockData] = useState({});

//   useEffect(() => {
//     const eventSource = new EventSource('http://127.0.0.1:5000/prices');
//     eventSource.onmessage = (event) => {
//       const data = JSON.parse(event.data);
//       setStockData(data);
//     };
    
//     return () => {
//       eventSource.close(); // Close the event source connection when the component unmounts
//     };
//   }, []);


//   return (
//     <div className="App">
//       <h1 className="text-2xl font-bold mb-4">Stock Prices</h1>
//       <div className="grid grid-cols-2 gap-4">
//         {Object.entries(stockData).map(([symbol, price]) => (
//           <div key={symbol} className="border p-4">
//             <p className="text-lg font-bold">{symbol}</p>
//             <p className="mt-2">${price.toFixed(2)}</p>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// export default App;
