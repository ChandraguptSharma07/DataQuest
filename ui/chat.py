"""
Security Expert Chatbot - Powered by Gemini
"""
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# System prompt - gives Gemini the security expert personality
SYSTEM_PROMPT = """You are SENTINEL, a senior cybersecurity analyst with 15 years experience.

Your personality:
- Direct and no-nonsense, but approachable
- You explain complex security concepts in plain English
- You occasionally use hacker slang (pwned, zero-day, exploit, CVE, etc.)
- You're slightly paranoid about security (in a good way)
- You give practical, actionable advice
- You reference real CVEs and attack patterns when relevant

Your expertise:
- Vulnerability analysis (CVEs, CVSS scoring)
- Malware analysis and incident response
- Network security and penetration testing
- Secure coding practices
- Threat intelligence

Rules:
- Keep responses concise (2-3 paragraphs max)
- Always recommend safe practices
- If asked about illegal hacking, redirect to ethical security practices
- Use bullet points for actionable steps
"""

def load_kb_for_chat():
    """Load knowledge base to give chat context about custom threats."""
    kb_text = ""
    if os.path.exists("knowledge_base.jsonl"):
        import json
        with open("knowledge_base.jsonl", "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if "learning" in entry:
                        name = entry.get('threat_name', entry['threat_id'])
                        kb_text += f"- {name} ({entry['threat_id']}): {entry['learning']}\n"
                    elif "analysis" in entry:
                        kb_text += f"- {entry['key']}: {entry['analysis'][:200]}...\n"
                except:
                    continue
    return kb_text

def init_chat():
    """Initialize the chat model with security persona + knowledge base."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    
    # Load KB context
    kb_context = load_kb_for_chat()
    
    # Dynamic system prompt with KB
    full_prompt = SYSTEM_PROMPT + f"""

IMPORTANT - YOUR KNOWLEDGE BASE:
You have learned about the following custom threats from this organization:
{kb_context if kb_context else "(No custom threats learned yet)"}

When users ask about these threats, use this knowledge!
"""
    
    # Try models in order of preference
    models = ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-pro']
    
    for m in models:
        try:
            model = genai.GenerativeModel(m, system_instruction=full_prompt)
            return model.start_chat(history=[])
        except:
            continue
            
    st.error("No Gemini models available. Check API Key.")
    return None

def render_chat():
    """Render the chat interface in Streamlit."""
    st.markdown("### 🤖 Ask SENTINEL")
    st.caption("Your AI security analyst • Ask about CVEs, malware, best practices")
    
    # Initialize chat session (without KB - we'll inject it per-message)
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = init_chat()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history in a scrollable container
    with st.container(height=500, border=False):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about security..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response with FRESH KB context
        if st.session_state.chat_session:
            try:
                # Reload KB on every message (real-time updates!)
                kb_context = load_kb_for_chat()
                
                # Prepend KB to user question if KB exists
                if kb_context:
                    augmented_prompt = f"""[KNOWLEDGE BASE - Use this first!]
{kb_context}

[USER QUESTION]
{prompt}"""
                else:
                    augmented_prompt = prompt
                
                response = st.session_state.chat_session.send_message(augmented_prompt)
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Error: {e}"
        else:
            reply = "🔒 API key not configured. Set GEMINI_API_KEY in .env"
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
