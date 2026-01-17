import json
import time
import random
import logging
from typing import List, Dict, Any

from utils.nist_client import fetch_real_cves

# Configure Logging to show the data mix
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [GENERATOR] - %(message)s')
logger = logging.getLogger(__name__)

# --- LOCAL DATABASE SIMULATION ---
# These threats simulate our "Internal/Local" threat intelligence database.
SIMULATED_LOCAL_THREATS = [
    {"threat_id": "SIM-001", "description": "Simulated SQL Injection in Login", "score": 9.8},
    {"threat_id": "SIM-002", "description": "Simulated XSS in Search Bar", "score": 6.5},
    {"threat_id": "SIM-003", "description": "Simulated Buffer Overflow in Payment Gateway", "score": 8.0}
]

def generate_stream():
    """
    Generates a hybrid stream of threats:
    1. Fetches REAL data from NIST API (Online Source).
    2. Injects SIMULATED data from local DB (Local Source).
    Demonstrates the pipeline's ability to fuse multiple intelligence sources.
    """
    logger.info("Starting Threat Stream Generator...")
    logger.info("Mode: HYBRID (Online NIST Feed + Local Simulation)")

    while True:
        try:
            # 1. ONLINE SOURCE: Fetch real CVEs from NIST
            logger.info("Fetching real-time data from NIST API...")
            real_cves = fetch_real_cves(limit=2)
            
            # Rename field to match our internal schema (id -> threat_id)
            for cve in real_cves:
                if "id" in cve:
                     cve["threat_id"] = cve.pop("id")
            
            logger.info(f"Received {len(real_cves)} real-time alerts.")

            # 2. LOCAL SOURCE: Inject a simulated threat to ensure we have matches
            # (Use a random choice to simulate specific targeted attacks)
            local_threat = random.choice(SIMULATED_LOCAL_THREATS)
            logger.info(f"Injecting local simulation data: {local_threat['threat_id']}")

            # 3. MERGE & STREAM
            mixed_batch = real_cves + [local_threat]
            
            with open("stream.jsonl", "a") as f:
                for threat in mixed_batch:
                    threat["timestamp"] = time.time()
                    f.write(json.dumps(threat) + "\n")
                    f.flush()
            
            logger.info(f" streamed {len(mixed_batch)} events to stream.jsonl")
            
            # Rate limit to avoid API bans and simulate realistic traffic
            time.sleep(5)
            
        except KeyboardInterrupt:
            logger.warning("Generator stopped by user.")
            break
        except Exception as e:
            logger.error(f"Stream generation error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    generate_stream()
