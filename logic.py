import pathway as pw
from ingest import get_data_sources
from utils.ai_helper import analyze_risk

# --- USER DEFINED FUNCTIONS (UDFs) ---

@pw.udf
def check_match(description: str, product: str) -> bool:
    """
    Case-insensitive match to check if a Product Name appears in a Threat Description.
    Handles potential Null/None values safely.
    """
    if not description or not product:
        return False
    return product.casefold() in description.casefold()

def run_pipeline():
    """
    Orchestrates the Zero-Day Cyber Sentinel Logic:
    1. Ingests Real-Time Threats (Online) & Asset Inventory (Static).
    2. JOINs them to find relevant threats to our specific infrastructure.
    3. Analyzes risk using Gemini AI.
    4. Outputs actionable alerts.
    """
    # 1. Ingest Data
    threats, inventory = get_data_sources()

    # 2. Windowing (Required for Streaming Joins)
    # We use a simplified window to join streaming data with static data
    threats = threats.with_columns(join_key=1)
    inventory = inventory.with_columns(join_key=1)

    # 3. The Core Logic: CROSS-JOIN + FILTER
    # "Show me all threats that mention my products"
    matches = threats.join(
        inventory,
        pw.left.join_key == pw.right.join_key
    ).filter(
        check_match(pw.this.description, pw.this.product)
    )

    # 4. Enrichment & Output
    # Create the final Alert object with AI Analysis
    alerts = matches.select(
        timestamp=pw.this.timestamp,
        threat_id=pw.this.threat_id,
        asset_id=pw.this.asset_id,
        description=pw.this.description,
        product=pw.this.product,
        analysis=pw.apply(analyze_risk, pw.this.description, pw.this.product),
    )

    # 5. Sink (Write to File for UI to consume)
    pw.io.jsonlines.write(alerts, "alerts.jsonl")
    
    # 6. Execute
    pw.run()

if __name__ == "__main__":
    run_pipeline()
