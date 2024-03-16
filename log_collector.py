import logging
import time
import os

def collect_logs(log_level=logging.INFO, log_file="system_logs.log"):
    """Collects logs and writes them to a file for persistence."""

    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    while True:
        try:
            logging.info("Collecting logs...")  # Example log message
            time.sleep(1)  # Adjust sleep time as needed
        except KeyboardInterrupt:  # Allow for graceful exit
            logging.info("Exiting log collection...")
            break

if __name__ == "__main__":
    try:
        collect_logs()  # Collect logs and write to the default file
    except Exception as e:  # Catch any unexpected errors
        logging.error("An error occurred: %s", str(e))