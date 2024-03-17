from log_collector import collect_logs
from log_parser import parse_logs
from log_storage import store_logs
from alerting import define_alerts
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_alert(alerts):
    """Sends an email alert with the status of the logs and the collected logs."""
    try:
        email_from = "mburujkaranja@gmail.com"
        email_to = "maura.karanja@gmail.com"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        username = "mburujkaranja@gmail.com"
        password = "your_password"  # Update with your actual password
        
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = 'SIEM Log Status and Alerts'

        # Construct email body with log status and alerts
        email_body = "Log Status:\n"
        email_body += "No errors detected. Logs collected successfully.\n\n"

        if not alerts.empty:
            email_body += "*Security Alert!*\n"
            email_body += str(alerts) + "\n\n"

        msg.attach(MIMEText(email_body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

def main():
    try:
        logs_df = collect_logs()
        parsed_logs = parse_logs(logs_df.copy())
        store_logs(parsed_logs)
        alerts = define_alerts(parsed_logs.copy())
        if not alerts.empty:
            print("*Security Alert!*")
            print(alerts)
        send_email_alert(alerts)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
