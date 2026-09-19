import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR/"data"/"bgp_events.db"

def get_connection():
    return sqlite3.connect(DATABASE_FILE)

def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                prefix TEXT NOT NULL,
                peer_asn TEXT,
                old_origin TEXT,
                new_origin TEXT,
                known_origins TEXT,
                rpki_status TEXT,
                path TEXT,
                score INTEGER,
                risk_level TEXT
            )"""
        )
def insert_event(event):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO events (
                timestamp,
                prefix,
                peer_asn,
                old_origin,
                new_origin,
                known_origins,
                rpki_status,
                path,
                score,
                risk_level
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (event.get("timestamp"),
            event.get("prefix"),
            str(event.get("peer_asn")) if event.get("peer_asn") is not None else None,
            str(event.get("old_origin")) if event.get("old_origin") is not None else None,
            str(event.get("new_origin")) if event.get("new_origin") is not None else None,
            json.dumps(event.get("known_origins", [])),
            event.get("rpki_status"),
            json.dumps(event.get("path", [])),
            event.get("score"),
            event.get("risk_level")
        ))
