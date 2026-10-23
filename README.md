# 🛰️ BGP Hijack Visualizer

> Real-time BGP monitoring and risk classification for Indian ISPs, built on live routing data.

The internet runs on BGP, a protocol built on trust. When an AS announces a prefix it doesn't own (a **BGP hijack** or route leak), traffic can be redirected, intercepted, or blackholed. This project watches live BGP announcements for major Indian networks, validates them, and ranks each update by risk so suspicious routes stand out.


---

## ✨ Features

- **Live ingestion**: streams real-time BGP updates from [RIPE RIS Live](https://ris-live.ripe.net/) over WebSocket, with auto-reconnect (ping/pong keepalive).
- **India-focused filtering**: tracks announcements and withdrawals involving Indian ISPs:

  | ISP | ASN |
  |---|---|
  | Jio | AS55836 |
  | Airtel | AS9498 |
  | Hathway | – |
  | VSNL / Tata | – |
  | Airtel Business | – |

- **RPKI validation**: checks each (origin ASN, prefix) pair against Cloudflare's RPKI validator.
- **Risk categorization**: every update is classified into a risk level based on its validation result and route attributes.
- **REST API**: FastAPI backend serving updates, alerts, and stats.
- **Persistent storage**: SQLite database for collected updates and classified alerts.
- **Web dashboard**: React frontend for browsing the live alert feed.

---

## 🏗️ Architecture

```
 RIPE RIS Live (WebSocket)
          │
          ▼
 ┌──────────────────┐     ┌────────────────────┐
 │  ingestion/      │────▶│  detection/        │
 │  stream + filter │     │  RPKI check + risk │
 └──────────────────┘     └─────────┬──────────┘
                                    │
                                    ▼
                          ┌──────────────────┐
                          │  SQLite          │
                          └─────────┬────────┘
                                    │
                                    ▼
                          ┌──────────────────┐        ┌────────────────┐
                          │  backend/        │───────▶│  frontend/     │
                          │  FastAPI         │  JSON  │  React         │
                          └──────────────────┘        └────────────────┘
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Ingestion & detection | Python, `asyncio`, `websockets`, `requests` |
| API | FastAPI |
| Database | SQLite |
| Frontend | React |
| Data sources | RIPE RIS Live, Cloudflare RPKI API |

---

## 🚦 Risk Levels

Each BGP update is assigned a risk level after RPKI validation and route checks.

| Level | Meaning |
|---|---|
| 🟢 **Low** | Valid route, origin matches the expected owner |
| 🟡 **Medium** | Not found in RPKI, or unusual but not clearly malicious |
| 🔴 **High** | RPKI **invalid**: origin ASN or prefix length doesn't match the published ROA |


---

## 📁 Project Structure

```
bgp-hijack-visualizer/
├── ingestion/      # RIPE RIS Live WebSocket client (ris_live.py)
├── detection/      # RPKI validation + risk classification
├── backend/        # FastAPI app and SQLite access
├── frontend/       # React dashboard
└── data/           # Collected BGP updates (newline-delimited JSON)
```

### Sample record

```json
{
  "type": "announcement",
  "isp": "Jio",
  "origin_asn": 55836,
  "prefix": "203.0.113.0/24",
  "path": [3356, 1299, 55836],
  "peer_asn": 3356,
  "timestamp": 1760000000
}
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### 1. Clone and set up Python

```bash
git clone https://github.com/<your-username>/bgp-hijack-visualizer.git
cd bgp-hijack-visualizer

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Start the ingestion stream

```bash
python ingestion/ris_live.py
```

### 3. Run the API

```bash
uvicorn backend.main:app --reload
```

Interactive docs are available at `http://localhost:8000/docs`.

### 4. Run the dashboard

```bash
cd frontend
npm install
npm start
```

> ✏️ *Update the file paths and commands above to match your actual entry points.*

---

## 🔌 API Overview

| Method | Endpoint | Description |
|---|---|---|
| GET | `/updates` | Recent BGP updates |
| GET | `/alerts` | Updates flagged above a risk threshold |
| GET | `/stats` | Counts by risk level and ISP |

> ✏️ *Replace with your real routes.*

---

## 🗺️ Roadmap

- [x] Live BGP ingestion via RIPE RIS Live
- [x] Indian ISP filtering
- [x] RPKI validation and risk categorization
- [x] FastAPI backend with SQLite storage
- [x] React frontend
- [ ] Interactive AS-path graph and world map
- [ ] Historical hijack replay
- [ ] Explainability layer: plain-language reasons for each alert
- [ ] LLM/AI-assisted analysis
- [ ] Deployment

---

## 🙏 Data Sources & Acknowledgements

- [RIPE RIS Live](https://ris-live.ripe.net/): real-time BGP feed
- [Cloudflare RPKI](https://rpki.cloudflare.com/): route origin validation
- [bgp.he.net](https://bgp.he.net/): reference for exploring ASes and prefixes

---

## 📄 License

MIT. See [LICENSE](LICENSE) for details.
