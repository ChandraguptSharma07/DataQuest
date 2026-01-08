import pathway as pw
from ingest import get_data_sources
from utils.ai_helper import analyze_risk

def run_pipeline():
    threats, inventory = get_data_sources()

    threats = threats.with_columns(join_key=1)
    inventory = inventory.with_columns(join_key=1)

    matches = threats.join(
        inventory,
        pw.left.join_key == pw.right.join_key
    ).filter(
        pw.this.description.to_lower().contains(pw.this.product.to_lower())
    )

    alerts = matches.select(
        timestamp=pw.this.timestamp,
        threat_id=pw.this.id,
        asset_id=pw.this.asset_id,
        description=pw.this.description,
        product=pw.this.product,
        analysis=pw.apply(analyze_risk, pw.this.description, pw.this.product),
    )

    pw.io.jsonlines.write(alerts, "alerts.jsonl")
    
    pw.run()

if __name__ == "__main__":
    run_pipeline()
