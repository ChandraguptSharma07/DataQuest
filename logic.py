import pathway as pw
from ingest import get_data_sources
from utils.ai_helper import analyze_risk

# --- UDFs ---

@pw.udf
def is_relevant(desc: str, prod: str) -> bool:
    # Basic null check + case insensitive match
    if not desc or not prod:
        return False
    return prod.casefold() in desc.casefold()

def run_pipeline():
    """
    Core RAG Pipeline: Joins Stream (Threats) with Static (Inventory).
    """
    # 1. Inputs
    threats, inventory = get_data_sources()

    # 2. Windowing Hack
    # Pathway requires windowing for streaming joins.
    # Using '1' as a dummy key effectively creates a global window for this simple use case.
    threats = threats.with_columns(join_key=1)
    inventory = inventory.with_columns(join_key=1)

    # 3. Cross Join + Filter
    matches = threats.join(
        inventory,
        pw.left.join_key == pw.right.join_key
    ).filter(
        is_relevant(pw.this.description, pw.this.product)
    )

    # 4. AI Enrichment
    # Note: AI calls can be slow, but Pathway handles async parallelization well.
    alerts = matches.select(
        timestamp=pw.this.timestamp,
        threat_id=pw.this.threat_id,
        asset_id=pw.this.asset_id,
        description=pw.this.description,
        product=pw.this.product,
        analysis=pw.apply(analyze_risk, pw.this.description, pw.this.product, pw.this.threat_id),
    )

    # 5. Output
    pw.io.jsonlines.write(alerts, "alerts.jsonl")
    
    # Let's go
    pw.run()

if __name__ == "__main__":
    run_pipeline()
