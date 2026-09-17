from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
EVENTS_FILE = "data/updates.jsonl"

@app.get("/")
def home():
    return {"message": "BGP-H-V API is running"}

@app.get("/events")
def get_events():
    events = []
    try:
        with open(EVENTS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
    except FileNotFoundError:
        print("File not found!")
        return []

    return events[-100:]

@app.get("/stats")
def get_stats():
    events = []
    try:
        with open(EVENTS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    events.append(json.loads(line))
    except FileNotFoundError:
        print("File not found!")
        return {
            "total_events": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
    stats = {
            "total_events": len(events),
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
    }
    for event in events:
        risk_level = event.get("risk_level", "").lower()
        if risk_level in stats:
            stats[risk_level] += 1
    return stats
    