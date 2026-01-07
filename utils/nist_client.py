import requests

def fetch_real_cves(api_key=None, limit=5):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {"apiKey": api_key} if api_key else {}
    params = {"resultsPerPage": limit}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        clean_cves = []
        for item in data.get("vulnerabilities", []):
            cve = item.get("cve", {})
            metrics = cve.get("metrics", {}).get("cvssMetricV31", [])
            score = metrics[0]["cvssData"]["baseScore"] if metrics else 5.0
            
            clean_cves.append({
                "id": cve.get("id"),
                "description": cve.get("descriptions", [{}])[0].get("value", "No description"),
                "score": score
            })
            
        return clean_cves

    except Exception:
        return []

if __name__ == "__main__":
    print(fetch_real_cves())
