import smtplib
from email.mime.text import MIMEText

# Configuration from app.py
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'heyram910@gmail.com'
EMAIL_PASS = 'eaqpzaqjukcikjhi' # Removed spaces

def test_smtp():
    print(f"Testing connection to {SMTP_SERVER}:{SMTP_PORT}...")
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1) # Show full debug output
        server.starttls()
        print("TLS Started.")
        
        print("Attempting login...")
        server.login(EMAIL_USER, EMAIL_PASS)
        print("Login Successful!")
        
        msg = MIMEText("This is a test email from HealthRisk AI Debugger.")
        msg['Subject'] = "SMTP Test Success"
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER # Send to self
        
        server.send_message(msg)
        print("Test Email Sent Successfully!")
        server.quit()
        
    except Exception as e:
        print(f"\n❌ SMTP ERROR: {e}")
        print("\nTroubleshooting Tips:")
        print("1. Check if 'App Password' is correct (remove spaces if copied weirdly).")
        print("2. Ensure 2-Step Verification is ON for the Google Account.")

if __name__ == '__main__':
    test_smtp()
