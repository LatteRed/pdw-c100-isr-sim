# operator/simulator/app.py
from flask import Flask
import random
import time
import json
import os

app = Flask(__name__)

# Get drone ID from environment (passed by Kubernetes)
DRONE_ID = os.getenv("DRONE_ID", "drone-unknown")
LAT_BASE = 37.7749   # San Francisco
LON_BASE = -122.4194

@app.route('/telemetry')
def telemetry():
    # Simulate realistic movement
    lat = LAT_BASE + random.uniform(-0.005, 0.005)
    lon = LON_BASE + random.uniform(-0.005, 0.005)
    data = {
        "id": DRONE_ID,
        "lat": round(lat, 6),
        "lon": round(lon, 6),
        "altitude": random.randint(80, 120),
        "speed": random.randint(20, 40),
        "heading": random.randint(0, 360),
        "battery": random.randint(60, 100),
        "timestamp": time.time()
    }
    return json.dumps(data)

@app.route('/health')
def health():
    return json.dumps({"status": "healthy", "drone_id": DRONE_ID})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
