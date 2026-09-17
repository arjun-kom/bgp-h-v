import { useEffect, useState } from "react";

function App(){
  const[stats, Setstats] = useState(null);

  useEffect(() =>{
    fetch("http://127.0.0.1:8000/stats")
    .then((response) => response.json())
    .then((data) => {
      Setstats(data);
    })
    .catch((error) =>{
      console.log("Error fetching stats: ", error);
    });
  }, []);

  return (
    <div>
      <h1>BGP Hijack Visualizer</h1>
      {stats ? (
        <div>
          <p>Total Events: {stats.total_events}</p>
          <p>Cirtical: {stats.critical}</p>
          <p>High: {stats.high}</p>
          <p>Medium: {stats.medium}</p>
          <p>Low: {stats.low}</p>
        </div>
      ):(
        <p>Loading Statistics...</p>
      )}
    </div>
  );
}

export default App;