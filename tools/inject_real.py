"""
inject_real_threat.py - Inject a REAL CVE that will match your inventory

This script:
1. Fetches the latest CVEs from NIST
2. Shows you the top 5
3. You pick one
4. It adds the affected product to your inventory.csv
5. Now when the stream runs, it will MATCH and trigger a real alert

Usage: python inject_real_threat.py
"""
import csv
import random
from utils.nist_client import fetch_real_cves

def main():
    print("\n🛡️ Real Threat Injector")
    print("=" * 40)
    
    # Fetch latest CVEs
    print("\n📡 Fetching latest CVEs from NIST...")
    cves = fetch_real_cves(limit=5)
    
    if not cves:
        print("❌ Failed to fetch CVEs. Check your network/API key.")
        return
    
    # Display options
    print(f"\n📋 Latest {len(cves)} CVEs:\n")
    for i, cve in enumerate(cves):
        cve_id = cve.get("id", "N/A")
        desc = cve.get("description", "No description")[:80]
        score = cve.get("score", 0)
        print(f"  [{i+1}] {cve_id} (Score: {score})")
        print(f"      {desc}...")
        print()
    
    # User picks one
    try:
        choice = int(input("Pick a CVE to inject (1-5): ")) - 1
        if choice < 0 or choice >= len(cves):
            print("Invalid choice.")
            return
    except ValueError:
        print("Enter a number.")
        return
    
    selected = cves[choice]
    cve_id = selected.get("id", "UNKNOWN")
    desc = selected.get("description", "")
    
    # Extract product name from description (crude but works)
    # Look for common patterns
    print(f"\n✅ Selected: {cve_id}")
    
    # Ask for product name
    print("\n🔍 What product does this CVE affect?")
    print("   (This will be added to your inventory so it matches)")
    product = input("   Product name: ").strip()
    
    if not product:
        # Try to guess from description
        words = desc.split()
        product = words[0] if words else "unknown_product"
        print(f"   Using: {product}")
    
    # Add to inventory
    new_asset = {
        "asset_id": f"auto-{random.randint(1000, 9999)}",
        "product": product.lower(),
        "version": "1.0.0",
        "priority": "critical"
    }
    
    with open("inventory.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["asset_id", "product", "version", "priority"])
        writer.writerow(new_asset)
    
    print(f"\n✅ Added to inventory.csv:")
    print(f"   {new_asset}")
    
    print(f"\n🎯 Next time '{product}' appears in a CVE description, it will MATCH!")
    print("   Restart the stream to see it in action.")
    print("\n💡 Tip: The description must contain the product name for matching.")
    print(f"   CVE says: '{desc[:100]}...'")

if __name__ == "__main__":
    main()
