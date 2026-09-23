from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import json
from datetime import datetime
import math

app = FastAPI(title="Architecture Acoustic Design API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AcousticMetrics(BaseModel):
    rt60: float
    sti: float
    frequency_response: dict
    spatial_metrics: dict
    timestamp: str

class StressEvent(BaseModel):
    timestamp: str
    gsr: float
    hrv: float
    temperature: float
    anxiety_score: float

# Initialize SQLite database
conn = sqlite3.connect('architecture-acoustic-design.db')
conn.execute('''CREATE TABLE IF NOT EXISTS acoustic_metrics
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 rt60 REAL,
                 sti REAL,
                 timestamp TEXT)''')
conn.execute('''CREATE TABLE IF NOT EXISTS stress_events
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 timestamp TEXT,
                 gsr REAL,
                 hrv REAL,
                 temperature REAL,
                 anxiety_score REAL)''')
conn.commit()
conn.close()

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/stress")
async def record_stress_event(event: StressEvent):
    conn = sqlite3.connect('architecture-acoustic-design.db')
    conn.execute(
        "INSERT INTO stress_events (timestamp, gsr, hrv, temperature, anxiety_score) VALUES (?, ?, ?, ?, ?)",
        (event.timestamp, event.gsr, event.hrv, event.temperature, event.anxiety_score)
    )
    conn.commit()
    conn.close()
    return {"status": "recorded", "id": event.timestamp}

@app.get("/api/v1/stress")
async def get_stress_events():
    conn = sqlite3.connect('architecture-acoustic-design.db')
    cursor = conn.execute("SELECT * FROM stress_events ORDER BY timestamp DESC LIMIT 100")
    events = cursor.fetchall()
    conn.close()
    return {
        "events": [
            {
                "timestamp": row[1],
                "gsr": row[2],
                "hrv": row[3],
                "temperature": row[4],
                "anxiety_score": row[5]
            } for row in events
        ]
    }

@app.post("/api/v1/acoustic")
async def record_acoustic_metrics(metrics: AcousticMetrics):
    conn = sqlite3.connect('architecture-acoustic-design.db')
    conn.execute(
        "INSERT INTO acoustic_metrics (rt60, sti, timestamp) VALUES (?, ?, ?)",
        (metrics.rt60, metrics.sti, metrics.timestamp)
    )
    conn.commit()
    conn.close()
    return {"status": "recorded", "id": metrics.timestamp}

@app.get("/api/v1/acoustic")
async def get_acoustic_metrics():
    conn = sqlite3.connect('architecture-acoustic-design.db')
    cursor = conn.execute("SELECT * FROM acoustic_metrics ORDER BY timestamp DESC LIMIT 100")
    metrics = cursor.fetchall()
    conn.close()
    return {
        "metrics": [
            {
                "rt60": row[1],
                "sti": row[2],
                "timestamp": row[3]
            } for row in metrics
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
