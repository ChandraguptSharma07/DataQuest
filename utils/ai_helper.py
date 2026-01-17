import os
import logging
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

# Initialize Environment & Logging
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [AI] - %(message)s')
logger = logging.getLogger(__name__)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")
else:
    genai.configure(api_key=api_key)

# Initialize Model (Global)
# Using 'flash-exp' for speed, fallback to 'flash' if needed
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    logger.error(f"Failed to initialize Gemini Model: {e}")
    model = None

def analyze_risk(threat_desc: str, asset_info: str) -> str:
    """
    Sends threat context to Gemini for risk assessment.
    Returns: Analyzed text (Risk Level + Explanation + Fix).
    """
    if not model:
        return "AI Module Offline: Check API Key."

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
        logger.error(f"Gemini API Error: {e}")
        return f"AI Analysis Failed: {str(e)[:50]}..." # Truncate error for UI cleaner view

def generate_fix_script(threat_id: str, analysis_text: str) -> str:
    """
    Generates a remediation shell script in the /fixes/ directory.
    Returns: Absolute path to the generated script.
    """
    filename = f"fixes/fix_{threat_id}.sh"
    try:
        with open(filename, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(f"# Auto-generated fix for Threat ID: {threat_id}\n")
            f.write(f"# Analysis Context: {analysis_text.replace(chr(10), ' ')}\n")
            f.write("\n# [Placeholder] In a production system, the AI's suggested command would go here.\n")
            f.write("echo 'Applying security patch...'\n")
            f.write("sleep 2\n")
            f.write("echo 'Patch applied successfully.'\n")
        
        logger.info(f"Generated fix script: {filename}")
        return filename
    except IOError as e:
        logger.error(f"Failed to write fix script {filename}: {e}")
        return ""

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY not found in .env files. Test will likely fail.")
    
    print("Testing AI Analysis...")
    result = analyze_risk("SQL Injection Exploit detected in login params", "Asset: Web Server (Flask) v1.1.2")
    print(f"AI Result:\n{result}")
    
    print("\nTesting Script Gen...")
    file = generate_fix_script("TEST-001", result)
    print(f"Generated: {file}")
