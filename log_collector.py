# log_collector.py
import logging
import os
import time
import subprocess
import win32evtlog
import winreg

def collect_logs(log_level=logging.INFO, log_file="system_logs.log"):
    """Collects logs and writes them to a file for persistence."""

    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        try:
            # Collect logs from the Windows Event Viewer
            events = win32evtlog.ReadEventLog(None, win32evtlog.EVENTLOG_SEQUENTIAL_READ | win32evtlog.EVENTLOG_BACKWARDS_READ, 0)
            for event in events:
                message = f"Event Type: {event.EventType}\nEvent ID: {event.EventID}\nEvent Time: {event.TimeGenerated}\nMessage: {event.StringInserts}"
                logging.info(message)

            # Monitor file system events and perform antivirus scanning
            for root, dirs, files in os.walk('C:\\'):  # Adjust the directory to monitor as needed
                for file in files:
                    file_path = os.path.join(root, file)
                    logging.info(f"File added/modified: {file_path}")
                    scan_for_malware(file_path)  # Perform antivirus scanning

            # Monitor registry changes
            reg_key = winreg.HKEY_LOCAL_MACHINE
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            reg_access = winreg.KEY_NOTIFY | winreg.KEY_READ  # Notify about changes and read access
            reg_hive = None
            reg_handle = winreg.OpenKey(reg_key, reg_path, 0, reg_access)
            winreg.NotifyChangeKeyValue(reg_handle, True, winreg.REG_NOTIFY_CHANGE_LAST_SET)

            while True:
                result = winreg.WaitForSingleObject(reg_handle, 500)  # Wait for registry changes (500 ms timeout)
                if result == winreg.WAIT_OBJECT_0:
                    logging.info("Registry change detected.")
                    # You can add code here to read the registry key values and log them
                    winreg.NotifyChangeKeyValue(reg_handle, True, winreg.REG_NOTIFY_CHANGE_LAST_SET)
                elif result == winreg.WAIT_TIMEOUT:
                    continue
                else:
                    logging.warning("Registry monitoring interrupted.")
                    break

            time.sleep(1)  # Adjust sleep time as needed
        except KeyboardInterrupt:  # Allow for graceful exit
            logging.info("Exiting log collection...")
            break
        except Exception as e:  # Catch any unexpected errors
            logging.error("An error occurred: %s", str(e))

def scan_for_malware(file_path):
    """Performs antivirus scanning on the specified file."""
    try:
        result = subprocess.run(['clamscan', '--quiet', '--stdout', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            logging.warning(f"Malware detected in file: {file_path}")
            logging.warning(result.stdout)
    except FileNotFoundError:
        logging.error("ClamAV is not installed or not found.")
    except Exception as e:
        logging.error(f"An error occurred during malware scanning: {e}")

if __name__ == "__main__":
    try:
        collect_logs()  # Collect logs and perform antivirus scanning
    except Exception as e:  # Catch any unexpected errors
        logging.error("An error occurred: %s", str(e))
