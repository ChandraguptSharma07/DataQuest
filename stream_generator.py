import json
import time
import random
import logging
from typing import List, Dict, Any

from utils.nist_client import fetch_real_cves

import json
import time
import random
import logging
from typing import List, Dict, Any

from utils.nist_client import fetch_real_cves

# Simplify logging format - less "enterprise", more pragmatic
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [GEN] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

# TODO: Move this to a proper DB later. For now, hardcoded is fine.
LOCAL_DATA = [
    {"threat_id": "SIM-001", "description": "Simulated SQL Injection in Login", "score": 9.8},
    {"threat_id": "SIM-002", "description": "Simulated XSS in Search Bar", "score": 6.5},
    {"threat_id": "SIM-003", "description": "Simulated Buffer Overflow in Payment Gateway", "score": 8.0}
]

def generate_stream():
    """
    Hybrid Stream: Merges online NIST data with our local sim data.
    """
    logger.info("Starting Hybrid Stream (NIST + Local)...")

    while True:
        try:
            # 1. Grab online data
            logger.info("Fetching NIST data...")
            real_cves = fetch_real_cves(limit=2)
            
            # Quick cleanup: id -> threat_id
            for cve in real_cves:
                if "id" in cve:
                     cve["threat_id"] = cve.pop("id")

            # 2. Inject local test data (randomly)
            # We need this to verify our matching logic actually works locally
            local_threat = random.choice(LOCAL_DATA)
            logger.info(f"Injecting local sim: {local_threat['threat_id']}")

            # 3. Flush to stream
            mixed_batch = real_cves + [local_threat]
            
            with open("stream.jsonl", "a") as f:
                for threat in mixed_batch:
                    threat["timestamp"] = time.time()
                    f.write(json.dumps(threat) + "\n")
                    f.flush()
            
            logger.info(f"Wrote {len(mixed_batch)} events.")
            
            # Don't hammer the API
            time.sleep(5)
            
        except KeyboardInterrupt:
            logger.warning("Stopping.")
            break
        except Exception as e:
            logger.error(f"Crash in generator: {e}")
            time.sleep(5) # Wait before retry

if __name__ == "__main__":
    generate_stream()
