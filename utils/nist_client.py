import logging
import requests
from typing import List, Dict, Any, Optional

# Constants
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
DEFAULT_TIMEOUT = 10

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_real_cves(api_key: Optional[str] = None, limit: int = 5, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Fetches CVEs with pagination support.
    """
    headers = {"apiKey": api_key} if api_key else {}
    params = {
        "resultsPerPage": limit,
        "startIndex": offset
    }

    try:
        logger.info(f"Connecting to NIST NVD API (Limit: {limit})...")
        response = requests.get(NVD_API_URL, headers=headers, params=params, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        
        payload = response.json()
        vulnerabilities = payload.get("vulnerabilities", [])
        
        logger.info(f"Successfully fetched {len(vulnerabilities)} raw records.")

        clean_cves = []
        for record in vulnerabilities:
            cve_data = record.get("cve", {})
            
            # Extract CVSS Score (Prioritize V3.1)
            metrics = cve_data.get("metrics", {}).get("cvssMetricV31", [])
            base_score = metrics[0]["cvssData"]["baseScore"] if metrics else 5.0
            
            # Extract Description (English)
            descriptions = cve_data.get("descriptions", [])
            desc_text = next((d["value"] for d in descriptions if d["lang"] == "en"), "No description available")

            clean_cves.append({
                "threat_id": cve_data.get("id"),
                "description": desc_text,
                "score": base_score
            })
            
        return clean_cves

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error contacting NIST API: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error parsing NIST data: {e}")
        return []

if __name__ == "__main__":
    # Quick functionality test
    cves = fetch_real_cves()
    for cve in cves:
        print(f"[{cve['score']}] {cve['threat_id']}: {cve['description'][:60]}...")
