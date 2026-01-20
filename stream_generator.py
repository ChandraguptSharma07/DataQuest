import json
import time
import random
import logging
import os
import html
from typing import List, Dict, Any
from utils.nist_client import fetch_real_cves

# Simple logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("Stream")

# Fake Data for mixing
LOCAL_DATA = [
    {"threat_id": "SIM-001", "description": "SQL Injection in Login Page", "score": 9.8},
    {"threat_id": "SIM-002", "description": "XSS in Search Bar", "score": 6.5},
    {"threat_id": "SIM-003", "description": "Buffer Overflow in Payment Gateway", "score": 8.0},

]

def check_manual_input():
    """
    Checks 'manual_input.txt' for on-demand injection (Demo Trick).
    """
    try:
        if os.path.exists("manual_input.txt"):
            # Atomic Read + Clear using 'r+'
            with open("manual_input.txt", "r+") as f:
                content = f.read().strip()
                if content:
                    # Security: Input Validation (XALKA Request)
                    if len(content) > 1024:
                        logger.warning("Manual input too long (max 1024). Ignoring.")
                        f.seek(0)
                        f.truncate()
                        return None
                        
                    f.seek(0)
                    f.truncate()
            
            if content:
                # Security: Sanitize input
                safe_desc = html.escape(content)
                # Log generic message
                logger.info("⚡ MANUAL OVERRIDE INJECTED")
                return {
                    "threat_id": f"MANUAL-{int(time.time())}",
                    "product": "Manual Override System",
                    "description": safe_desc,
                    "score": 10.0 # Critical by default
                }
    except IOError as e:
        logger.warning(f"File I/O Error in manual check: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in manual check: {e}")
    return None

def generate_stream():
    """
    Hybrid Stream: NIST data + manual overrides (no auto-simulated data).
    """
    logger.info("Starting Stream (NIST + Manual)...")

    # Create the manual input file if it doesn't exist
    if not os.path.exists("manual_input.txt"):
        with open("manual_input.txt", "w") as f:
            f.write("")

# Local Fake Data (as requested)
LOCAL_DATA = [
    {"threat_id": "SIM-001", "description": "Simulated SQL Injection in Login", "score": 9.8},
    {"threat_id": "SIM-002", "description": "Simulated XSS in Search Bar", "score": 6.5},
    {"threat_id": "SIM-003", "description": "Simulated Buffer Overflow in Payment Gateway", "score": 8.0},

]

# ... [check_manual_input remains unchanged] ...

def generate_stream():
    """
    Hybrid Stream: Random NIST history + Occasional Simulated Fake Data.
    """
    # ... [startup code remains unchanged] ...

    seen_ids = set()

    while True:
        try:
            # Read Config (Deduplication Check)
            dedup_on = False
            try:
                if os.path.exists("stream_config.json"):
                    with open("stream_config.json", "r") as f:
                        config = json.load(f)
                        dedup_on = config.get("deduplicate", False)
            except:
                pass # Ignore config read errors

            # 1. Grab random data from recent history (Simulate diverse stream)
            rand_offset = random.randint(0, 2000)
            logger.info(f"Fetching NIST data (Offset: {rand_offset}) [Dedup: {dedup_on}]...")
            real_cves = fetch_real_cves(limit=2, offset=rand_offset)
            
            # Quick cleanup: id -> threat_id
            for cve in real_cves:
                if "id" in cve:
                     cve["threat_id"] = cve.pop("id")

            # Deduplication Filter
            if dedup_on:
                new_cves = []
                for cve in real_cves:
                    if cve["threat_id"] not in seen_ids:
                        new_cves.append(cve)
                        seen_ids.add(cve["threat_id"])
                    else:
                        logger.info(f"🚫 Skipped Duplicate: {cve['threat_id']}")
                real_cves = new_cves

            # 2. Check for Manual Override
            manual_threat = check_manual_input()
            
            # 3. Flush to stream (NIST + manual + occasional fake)
            mixed_batch = real_cves
            
            # Add Manual Override
            if manual_threat:
                mixed_batch.append(manual_threat)
                
            # Add Random Fake Threat (10% chance) - As requested "keep a few fake ones"
            if random.random() < 0.1:
                fake = random.choice(LOCAL_DATA).copy()
                fake["timestamp"] = time.time()
                mixed_batch.append(fake)
                logger.info(f"🎲 Injected Random Fake: {fake['threat_id']}")

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
