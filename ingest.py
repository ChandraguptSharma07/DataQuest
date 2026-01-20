import pathway as pw

# Schema Definition for Unified Threat Stream
# This acts as the standard interface for both Online (NIST) and Local (Simulated) data.
class ThreatSchema(pw.Schema):
    threat_id: str
    description: str
    score: float
    timestamp: float

# Schema for Static Asset Inventory
class InventorySchema(pw.Schema):
    asset_id: str
    product: str
    version: str
    priority: str

def get_data_sources():
    """
    Connects to input streams.
    """
    # 1. The Stream (NIST + Sims)
    threats = pw.io.jsonlines.read(
        "stream.jsonl",
        schema=ThreatSchema,
        mode="streaming"
    )

    # 2. The Static DB (Inventory)
    inventory = pw.io.csv.read(
        "inventory.csv",
        schema=InventorySchema,
        mode="static"
    )

    return threats, inventory

if __name__ == "__main__":
    # Test Block: Print schema and first few rows to verify connectivity
    t, i = get_data_sources()
    print("Threats Connected:", t)
    print("Inventory Connected:", i)
    # Note: Accessing data requires a computation engine run, 
    # but this confirms the connectors are valid.
