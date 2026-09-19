from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_connection, initialize_database
import json

app = FastAPI()
initialize_database()

#gotta change the fields before deployment
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def home():
    return {"message": "BGP-H-V API is running"}

@app.get("/events")
def get_events():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT 200
        """).fetchall()
    events = []

    for row in rows:
        events.append({
            "id": row[0],
            "timestamp": row[1],
            "prefix": row[2],
            "peer_asn": row[3],
            "old_origin": row[4],
            "new_origin": row[5],
            "known_origins": json.loads(row[6]) if row[6] else [],
            "rpki_status": row[7],
            "path": json.loads(row[8]) if row[8] else [],
            "score": row[9],
            "risk_level": row[10]
        })
    return events

@app.get("/stats")
def get_stats():
    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0]
        rows = connection.execute("""
            SELECT risk_level, COUNT(*)
            FROM events
            GROUP BY risk_level
        """).fetchall()
    
    stats = {
            "total_events": total,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
    }
    for risk_level, count in rows:
        risk_level = risk_level.lower()
        if risk_level in stats:
            stats[risk_level] += count
    return stats
