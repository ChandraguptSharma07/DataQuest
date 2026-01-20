"""
inject_full.py - One-Command Threat + Inventory Injection

Usage:
  python tools/inject_full.py "threat_name" "description" ["optional AI knowledge"]

Example:
  python tools/inject_full.py "fake_virus_of_CICs" "Critical malware detected in system" "This is a Level 10 rootkit that steals credentials"

What it does:
  1. Adds threat_name to inventory.csv (so Sentinel watches for it)
  2. Injects the threat into stream.jsonl (simulates detection)
  3. (Optional) Pre-teaches AI with custom knowledge
  4. Result: Alert fires immediately + AI responds with your knowledge
"""
import sys
import json
import time
import os

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("Error: Need at least threat_name and description.")
        sys.exit(1)
    
    threat_name = sys.argv[1]
    description = sys.argv[2]
    knowledge = sys.argv[3] if len(sys.argv) > 3 else None
    
    threat_id = f"CUSTOM-{int(time.time())}"
    
    # 1. Add to Inventory (so it matches)
    inventory_line = f"custom-{int(time.time())},{threat_name},1.0,critical\n"
    with open("inventory.csv", "a") as f:
        f.write(inventory_line)
    print(f"✅ Added to Inventory: {threat_name}")
    
    # 2. Inject into Stream
    threat = {
        "threat_id": threat_id,
        "threat_name": threat_name,
        "description": f"{description} ({threat_name})",
        "score": 10.0,
        "timestamp": time.time()
    }
    with open("stream.jsonl", "a") as f:
        f.write(json.dumps(threat) + "\n")
    print(f"✅ Injected into Stream: {threat_id}")
    
    # 3. Pre-teach AI (optional)
    if knowledge:
        entry = {
            "threat_id": threat_id,
            "threat_name": threat_name,
            "learning": knowledge
        }
        with open("knowledge_base.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"✅ Pre-taught AI: {knowledge}")
    
    print(f"\n🚨 Sentinel will now alert on '{threat_name}' threats!")
    print("   Open the dashboard to see the alert fire in real-time.")

if __name__ == "__main__":
    main()
