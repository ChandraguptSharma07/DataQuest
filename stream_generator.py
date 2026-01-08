import time
import json
import random
from utils.nist_client import fetch_real_cves

def generate_stream():
    simulated_threats = [
        {"id": "SIM-001", "description": "Simulated SQL Injection in Login", "score": 9.8},
        {"id": "SIM-002", "description": "Simulated XSS in Search Bar", "score": 6.5},
        {"id": "SIM-003", "description": "Simulated Buffer Overflow", "score": 8.0}
    ]

    while True:
        try:
            real_cves = fetch_real_cves(limit=2)
            
            mixed_batch = real_cves + [random.choice(simulated_threats)]
            
            with open("stream.jsonl", "a") as f:
                for threat in mixed_batch:
                    threat["timestamp"] = time.time()
                    f.write(json.dumps(threat) + "\n")
                    f.flush()
            
            time.sleep(5)
            
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    generate_stream()
