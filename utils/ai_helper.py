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

# Valid models in priority order
MODELS = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-pro']

model = None
for m in MODELS:
    try:
        model = genai.GenerativeModel(m)
        model.generate_content("test") # quick check
        logger.info(f"Connected to {m}")
        break
    except:
        continue # Try next

if not model:
    logger.error("Could not connect to any Gemini models.")

# =============================================================================
# KNOWLEDGE BASE & AUTO-LEARN
# Agreed Design (XALKA Consensus 2026-01-20):
# - TTL=0 for demo (infinite cache), configurable for production.
# - Key format: {threat_id}_{sha256(desc)[:16]}
# - Graceful degradation on cache errors.
# =============================================================================
import json
import hashlib

KB_FILE = "knowledge_base.jsonl"
DEMO_MODE = True  # Set to False in production for TTL-based caching

def make_kb_key(threat_id: str, desc: str) -> str:
    """Generate unique cache key using threat_id + description hash."""
    hash_part = hashlib.sha256(desc[:100].encode()).hexdigest()[:16]
    return f"{threat_id}_{hash_part}"

def get_from_kb(key: str) -> str | None:
    """Check if analysis for this key exists in KB (cache hit)."""
    if not os.path.exists(KB_FILE):
        return None
    try:
        with open(KB_FILE, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("key") == key:
                        logger.info(f"🎯 Cache HIT: {key}")
                        return entry.get("analysis")
                except:
                    continue
    except IOError as e:
        logger.warning(f"Cache read error: {e}")
    return None

def save_to_kb(key: str, analysis: str):
    """Auto-save analysis to KB (cache write). Graceful on error."""
    try:
        entry = {"key": key, "analysis": analysis}
        with open(KB_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"💾 Auto-cached: {key}")
    except IOError as e:
        logger.warning(f"Cache write failed (graceful): {e}")

def teach_ai(threat_id, learning):
    """Manual override - adds a rule to the brain."""
    entry = {"threat_id": threat_id, "learning": learning}
    try:
        with open(KB_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        logger.info(f"🧠 Learned: {learning}")
    except IOError as e:
        logger.warning(f"Teach failed: {e}")

def load_manual_rules() -> str:
    """Load manually taught rules (not auto-cached analyses)."""
    kb_text = ""
    if os.path.exists(KB_FILE):
        try:
            with open(KB_FILE, "r") as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if "learning" in entry:  # Manual rule, not auto-cache
                            kb_text += f"- Rule: If threat is '{entry['threat_id']}', note that {entry['learning']}\n"
                    except:
                        continue
        except IOError:
            pass
    return kb_text

def analyze_risk(desc: str, asset: str, threat_id: str = "") -> str:
    """
    Asks Gemini to analyze the threat.
    AUTO-LEARN: Caches analysis after first call. Returns cached on repeat.
    """
    if not model:
        return "AI Offline."
    
    # Generate cache key
    cache_key = make_kb_key(threat_id, desc)
    
    # Check cache first (Demo Mode = infinite TTL)
    cached = get_from_kb(cache_key)
    if cached:
        return cached  # Return cached analysis
    
    # Cache miss - call AI
    manual_rules = load_manual_rules()
    prompt = f"""
    Context:
    You are a security analyst. 
    Use these KNOWN RULES if applicable:
    {manual_rules}
    
    Current Event:
    Threat ID: {threat_id}
    Threat Desc: {desc}
    Asset: {asset}
    
    Task:
    1. Risk Level (Low/High/Critical)
    2. One-line why.
    3. Bash fix command.
    """
    
    try:
        analysis = model.generate_content(prompt).text
        
        # AUTO-LEARN: Save to cache for future
        save_to_kb(cache_key, analysis)
        
        return analysis
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
