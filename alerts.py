import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

def send_spike_email(spikes):
    if not spikes:
        return

    subject = f"🚀 POE Spike Alert — {len(spikes)} item(s) spiking!"

    body = "The following items are spiking right now:\n\n"
    for spike in spikes:
        body += f"• {spike['name']} ({spike.get('item_type', 'Unknown')})\n"
        body += f"  Price: {spike['chaos_value']}c | Change: +{spike['change']}%\n\n"

    body += "\nCheck your dashboard for more details!"

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print(f"📧 Spike alert email sent for {len(spikes)} item(s)!")
    except Exception as e:
        print(f"❌ Email failed: {e}")