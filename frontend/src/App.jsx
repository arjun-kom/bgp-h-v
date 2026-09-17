import { useEffect, useMemo, useState } from "react";
import "./App.css";

const FILTERS = ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"];

function App() {
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [darkMode, setDarkMode] = useState(true);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [filter, setFilter] = useState("ALL");

  useEffect(() => {
    const fetchData = () => {
      Promise.all([
        fetch("http://127.0.0.1:8000/stats").then((response) =>
          response.json()
        ),
        fetch("http://127.0.0.1:8000/events").then((response) =>
          response.json()
        ),
      ])
        .then(([statsData, eventsData]) => {
          setStats(statsData);
          setEvents(eventsData);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    };

    fetchData();

    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const filteredEvents = useMemo(() => {
    if (filter === "ALL") return events;
    return events.filter(
      (event) => event.risk_level.toUpperCase() === filter
    );
  }, [events, filter]);

  const countFor = (level) => {
    if (level === "ALL") return events.length;
    return events.filter((e) => e.risk_level.toUpperCase() === level).length;
  };

  return (
    <div className={darkMode ? "app dark" : "app light"}>
      <header className="top-bar">
        <div>
          <h1>BGP Hijack Visualizer</h1>
          <p>Real-time internet routing anomaly monitor</p>
        </div>

        <button
          className="theme-button"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? "☀️ Light mode" : "🌙 Dark mode"}
        </button>
      </header>

      <main>
        <section className="stats-grid">
          {stats ? (
            <>
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
            </>
          ) : (
            <p className="loading-text">Loading statistics...</p>
          )}
        </section>

        <section className="events-section">
          <div className="events-section-header">
            <h2>Detected Events</h2>

            <div className="filter-bar" role="group" aria-label="Filter by risk level">
              {FILTERS.map((level) => (
                <button
                  key={level}
                  className={`filter-pill ${level.toLowerCase()} ${
                    filter === level ? "active" : ""
                  }`}
                  onClick={() => setFilter(level)}
                >
                  {level.charAt(0) + level.slice(1).toLowerCase()}
                  <span className="filter-count">{countFor(level)}</span>
                </button>
              ))}
            </div>
          </div>

          {events.length === 0 ? (
            <p className="empty-text">No events detected yet.</p>
          ) : filteredEvents.length === 0 ? (
            <p className="empty-text">No events match this filter.</p>
          ) : (
            <div className="feed">
              {filteredEvents.map((event, index) => (
                <article
                  className={`feed-row ${event.risk_level.toLowerCase()}`}
                  key={`${event.timestamp}-${index}`}
                  style={{ animationDelay: `${Math.min(index, 14) * 0.05}s` }}
                  onClick={() => setSelectedEvent(event)}
                >
                  <span className="feed-dot" />

                  <div className="feed-body">
                    <div className="feed-top">
                      <span
                        className={`risk-badge ${event.risk_level.toLowerCase()}`}
                      >
                        {event.risk_level}
                      </span>
                      <span className="feed-title">
                        Possible BGP Route Anomaly
                      </span>
                      <span className="score">Score {event.score}</span>
                      <span className="event-time">
                        {formatTimestamp(event.timestamp)}
                      </span>
                    </div>

                    <div className="feed-details">
                      <span>
                        <em>Prefix</em> {event.prefix}
                      </span>
                      <span>
                        <em>Peer ASN</em> {event.peer_asn}
                      </span>
                      <span>
                        <em>New Origin</em> {event.new_origin}
                      </span>
                      <span>
                        <em>RPKI</em> {event.rpki_status}
                      </span>
                      <span className="feed-path">
                        <em>AS Path</em>{" "}
                        {event.path ? event.path.join(" → ") : "Unavailable"}
                      </span>
                    </div>
                  </div>

                  <button
                    className="details-button"
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedEvent(event);
                    }}
                  >
                    View more
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>

        {selectedEvent && (
          <div className="details-panel">
            <div className="details-content">
              <button
                className="close-button"
                onClick={() => setSelectedEvent(null)}
              >
                ✕
              </button>

              <h2>Event Details</h2>

              <p>
                <strong>Prefix:</strong> {selectedEvent.prefix}
              </p>

              <p>
                <strong>Peer ASN:</strong> {selectedEvent.peer_asn}
              </p>

              <p>
                <strong>Old Origin:</strong>{" "}
                {selectedEvent.old_origin ?? "None"}
              </p>

              <p>
                <strong>New Origin:</strong> {selectedEvent.new_origin}
              </p>

              <p>
                <strong>Known Origins:</strong>{" "}
                {selectedEvent.known_origins.join(", ")}
              </p>

              <p>
                <strong>RPKI Status:</strong> {selectedEvent.rpki_status}
              </p>

              <p>
                <strong>AS Path:</strong>{" "}
                {selectedEvent.path.join(" → ")}
              </p>

              <p>
                <strong>Risk Score:</strong> {selectedEvent.score}
              </p>

              <p>
                <strong>Risk Level:</strong> {selectedEvent.risk_level}
              </p>

              <p>
                <strong>Detected At:</strong>{" "}
                {formatTimestamp(selectedEvent.timestamp)}
              </p>

              <h3>Why was this flagged?</h3>

              <p>
                This event was flagged because the detector identified a
                possible routing anomaly involving the announced prefix,
                origin ASN, and AS path. The score was generated by the
                detector's configured heuristics.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;