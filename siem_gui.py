import tkinter as tk
from tkinter import scrolledtext
from alerting import define_alerts
from log_parser import parse_logs
from log_collector import collect_logs

def display_logs_and_alerts():
    # Collect logs
    logs_df = collect_logs()

    # Parse logs
    parsed_logs = parse_logs(logs_df.copy())

    # Define alerts
    alerts = define_alerts(parsed_logs.copy())

    # Display logs and alerts in GUI
    log_text.insert(tk.END, "Logs:\n")
    log_text.insert(tk.END, logs_df.to_string(index=False) + "\n\n")

    log_text.insert(tk.END, "Alerts:\n")
    if not alerts.empty:
        log_text.insert(tk.END, alerts.to_string(index=False))
    else:
        log_text.insert(tk.END, "No alerts found.")

# Create GUI window
window = tk.Tk()
window.title("SIEM Dashboard")

# Create scrolled text widget to display logs and alerts
log_text = scrolledtext.ScrolledText(window, width=80, height=20)
log_text.grid(row=0, column=0, padx=10, pady=10)

# Create button to trigger log collection and display
collect_button = tk.Button(window, text="Collect Logs", command=display_logs_and_alerts)
collect_button.grid(row=1, column=0, padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
