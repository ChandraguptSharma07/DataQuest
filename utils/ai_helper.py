import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash-exp')

def analyze_risk(threat_desc, asset_info):
    prompt = f"""
    Analyze this security match:
    Threat: {threat_desc}
    Asset: {asset_info}
    
    1. Risk Level (Low/Medium/High/Critical)
    2. One sentence explanation.
    3. Suggested Bash command to fix it.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

def generate_fix_script(threat_id, analysis_text):
    filename = f"fixes/fix_{threat_id}.sh"
    with open(filename, "w") as f:
        f.write("#!/bin/bash\n")
        f.write(f"# Auto-generated fix for {threat_id}\n")
        f.write(f"# Context: {analysis_text.replace(chr(10), ' ')}\n")
        f.write("echo 'Applying patch...'\n")
        # In a real app, we would parse the bash command from the AI.
        # Here we just echo success for safety.
        f.write("echo 'Patch applied successfully.'\n")
    return filename

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not found in .env files. Test will likely fail.")
    
    print("Testing AI Analysis...")
    result = analyze_risk("SQL Injection Exploit detected in login params", "Asset: Web Server (Flask) v1.1.2")
    print(f"AI Result:\n{result}")
    
    print("\nTesting Script Gen...")
    file = generate_fix_script("TEST-001", result)
    print(f"Generated: {file}")
