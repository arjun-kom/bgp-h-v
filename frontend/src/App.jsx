import { useEffect, useState } from "react";
import './App.css';

function App(){
  const[stats, Setstats] = useState(null);
  useEffect(() =>{
    const fetchStats = () => {
      fetch("http://127.0.0.1:8000/stats")
        .then((response) => response.json())
        .then((data) => {
          Setstats(data);
        })
        .catch((error) =>{
          console.log("Error fetching stats: ", error);
        });
    };
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval)
  }, []);

  return (
    <div className="dashboard">
      <h1>BGP Hijack Visualizer</h1>
      <h1 className="subtitle">
        Real-time internet routing anomaly monitor
      </h1>

      {stats ? (
        <div className="stats-grid">
          <div className="stat-card total">
            <h2>Total Events</h2>
            <p>{stats.total_events}</p>
          </div>

          <div className="stat-card critical">
            <h2>Critical</h2>
            <p>{stats.critical}</p>
          </div>

          <div className="stat-card high">
            <h2>High</h2>
            <p>{stats.high}</p>
          </div>

          <div className="stat-card medium">
            <h2>Medium</h2>
            <p>{stats.medium}</p>
          </div>

          <div className="stat-card low">
            <h2>Low</h2>
            <p>{stats.low}</p>
          </div>
        </div>
      ) : (
        <p>Loading statistics...</p>
      )}
    </div>
  );
}

export default App;