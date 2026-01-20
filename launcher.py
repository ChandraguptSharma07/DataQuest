import subprocess
import signal
import sys
import time
import logging

# Configure pragmatic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [LAUNCHER] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

procs = []

def cleanup(signum, frame):
    """Graceful shutdown: Try terminate, wait 10s, then force kill."""
    logger.info(f"🛑 Received signal {signum}. Shutting down services...")
    try:
        for p in procs:
            try:
                p.terminate()
            except OSError:
                pass # Already dead

        # Give them time to die gracefully
        logger.info("⏳ Waiting 5s for processes to exit...")
        start = time.time()
        while time.time() - start < 5:
            if all(p.poll() is not None for p in procs):
                sys.exit(0)
            time.sleep(0.5)

        # Force Kill if still stubborn
        logger.warning("💀 Force killing stubborn processes...")
        for p in procs:
            if p.poll() is None:
                try:
                    p.kill()
                except OSError:
                    pass
    finally:
        sys.exit(0)

# Register Signal Handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def start_service(command):
    """Spawns a subprocess and adds it to the list."""
    try:
        # We forward stdout/stderr to the main container log for visibility
        p = subprocess.Popen(command, stdout=sys.stdout, stderr=sys.stderr)
        procs.append(p)
        logger.info(f"✅ Started: {' '.join(command)}")
        return p
    except Exception as e:
        logger.error(f"❌ Failed to start {' '.join(command)}: {e}")
        cleanup(0, 0)

if __name__ == "__main__":
    logger.info("🚀 Booting Zero-Day Cyber Sentinel (Docker Singleton Mode)...")

    # --- DIAGNOSTIC START ---
    try:
        import google.generativeai as genai
        import os
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            logger.info("🔍 Checking available Gemini models...")
            models = [m.name for m in genai.list_models()]
            logger.info(f"📋 Available Models: {models}")
        else:
            logger.warning("⚠️ GEMINI_API_KEY not found during startup check.")
    except Exception as e:
        logger.error(f"❌ Diagnostic failed: {e}")
    # --- DIAGNOSTIC END ---

    # 1. Stream Generator (Data Source)
    start_service(["python", "stream_generator.py"])
    
    # 2. Logic Engine (The Brains)
    start_service(["python", "logic.py"])
    
    # 3. Streamlit UI (The Interface)
    # Using '0.0.0.0' for Docker binding
    start_service(["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"])

    # Monitor Loop
    logger.info("👀 Supervisor Active. Monitoring subprocesses...")
    while True:
        for p in procs:
            if p.poll() is not None:
                # If ANY service dies, the container should die to trigger a restart policy
                logger.error(f"🚨 CRITICAL: Service PID {p.pid} died! Aborting container.")
                cleanup(0, 0)
        time.sleep(2)
