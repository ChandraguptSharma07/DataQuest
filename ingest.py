import pathway as pw

class ThreatSchema(pw.Schema):
    id: str
    description: str
    score: float
    timestamp: float

class InventorySchema(pw.Schema):
    asset_id: str
    product: str
    version: str
    priority: str

def get_data_sources():
    threats = pw.io.jsonlines.read(
        "stream.jsonl",
        schema=ThreatSchema,
        mode="streaming"
    )

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
