"""
inject_sim_threat.py - Manually inject simulated threats from terminal

Usage: python inject_sim_threat.py
"""
import json
import time

# Predefined simulated threats
SIMULATED_THREATS = [
    {"threat_id": "SIM-001", "description": "Simulated SQL Injection in Login", "score": 9.8},
    {"threat_id": "SIM-002", "description": "Simulated XSS in Search Bar", "score": 6.5},
    {"threat_id": "SIM-003", "description": "Simulated Buffer Overflow in Payment Gateway", "score": 8.0},
    {"threat_id": "SIM-004", "description": "Simulated Path Traversal in File Upload", "score": 7.2},
    {"threat_id": "SIM-005", "description": "Simulated Remote Code Execution in API", "score": 10.0},
]

import sys

# ... [SIMULATED_THREATS definition logic remains if needed, or simplified] ...
# Using the existing format but adding CLI arg support

def main():
    # If arguments provided, use them for instant injection
    if len(sys.argv) > 1:
        custom_desc = " ".join(sys.argv[1:])
        threat = {
            "threat_id": f"CLI-{int(time.time())}",
            "product": "Manual CLI Injection",
            "description": custom_desc,
            "score": 10.0, # Default to critical if manual
            "timestamp": time.time()
        }
        
        with open("stream.jsonl", "a") as f:
            f.write(json.dumps(threat) + "\n")
            
        print(f"✅ Instantly Injected: {custom_desc}")
        return

    # Interactive Mode (Original)
    print("\n🎭 Simulated Threat Injector")
    # ... [rest of interactive logic] ...
    print("\nAvailable simulated threats:\n")
    for i, threat in enumerate(SIMULATED_THREATS):
        print(f"  [{i+1}] {threat['threat_id']}: {threat['description']} (Score: {threat['score']})")
    
    print(f"  [{len(SIMULATED_THREATS)+1}] Custom threat")
    
    # Get choice
    try:
        choice = int(input(f"\nSelect threat (1-{len(SIMULATED_THREATS)+1}): ")) - 1
        
        if choice < 0 or choice > len(SIMULATED_THREATS):
            print("Invalid choice.")
            return
        
        # Custom threat
        if choice == len(SIMULATED_THREATS):
            print("\n📝 Custom Threat")
            threat_id = input("  Threat ID (e.g., SIM-999): ").strip() or f"SIM-{int(time.time())}"
            description = input("  Description: ").strip() or "Custom simulated threat"
            score = float(input("  Score (0-10): ").strip() or "5.0")
            
            threat = {
                "threat_id": threat_id,
                "description": description,
                "score": score
            }
        else:
            threat = SIMULATED_THREATS[choice].copy()
        
        # Add timestamp
        threat["timestamp"] = time.time()
        
        # Inject to stream
        with open("stream.jsonl", "a") as f:
            f.write(json.dumps(threat) + "\n")
        
        print(f"\n✅ Injected: {threat['threat_id']}")
        print(f"   {threat['description']}")
        print(f"   Score: {threat['score']}")
        print("\n💡 Check the dashboard to see it appear!")
        
    except ValueError:
        print("Please enter a number.")
    except KeyboardInterrupt:
        print("\n\nCancelled.")

if __name__ == "__main__":
    main()
