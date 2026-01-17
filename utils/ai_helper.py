import os
import logging
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Simple logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [AI] %(message)s')
logger = logging.getLogger(__name__)

# API Key Check
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.warning("No API Key. AI is disabled.")
else:
    genai.configure(api_key=api_key)

# Global model init
try:
    # Use flash-exp because it's faster
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
except Exception as e:
    logger.error(f"Model init failed: {e}")
    model = None

def analyze_risk(desc: str, asset: str) -> str:
    """
    Asks Gemini to analyze the threat.
    """
    if not model:
        return "AI Offline."

    # Keep prompt simple and direct
    prompt = f"""
    Context:
    Threat: {desc}
    Asset: {asset}
    
    Task:
    1. Risk Level (Low/High/Critical)
    2. One-line why.
    3. Bash fix command.
    """
    
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        logger.error(f"GenAI Error: {e}")
        return "Analysis Failed."

def generate_fix_script(tid: str, analysis: str) -> str:
    """
    Writes a dummy fix script to disk.
    """
    path = f"fixes/fix_{tid}.sh"
    try:
        with open(path, "w") as f:
            f.write(f"#!/bin/bash\n# Fix for {tid}\n# {analysis.replace(chr(10), ' ')}\n")
            f.write("echo 'Patching...'\n")
            f.write("sleep 1\n")
            f.write("echo 'Done.'\n")
        
        logger.info(f"Created script: {path}")
        return path
    except Exception as e:
        logger.error(f"Write failed: {e}")
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
