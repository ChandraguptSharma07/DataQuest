import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_alert_email(alert_data: dict):
    """Send email alert for critical threats."""
    
    # Email config from env
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("ALERT_EMAIL")
    sender_password = os.getenv("ALERT_EMAIL_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    if not all([sender_email, sender_password, recipient_email]):
        logger.warning("Email not configured. Skipping email alert.")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🚨 CRITICAL THREAT DETECTED: {alert_data.get('product', 'Unknown')}"
        
        # Email body
        body = f"""
Critical Security Alert from Zero-Day Sentinel

Threat ID: {alert_data.get('threat_id', 'N/A')}
Product: {alert_data.get('product', 'Unknown')}
Score: {alert_data.get('score', 0)}

Description:
{alert_data.get('description', 'No description')}

AI Analysis:
{alert_data.get('analysis', 'No analysis available')}

---
This is an automated alert from your Zero-Day Cyber Sentinel system.
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        logger.info(f"✅ Email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return False
