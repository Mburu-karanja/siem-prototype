from log_collector import collect_logs
from log_parser import parse_logs
from log_storage import store_logs
from alerting import define_alerts

def main():
    logs_df = collect_logs()
    parsed_logs = parse_logs(logs_df.copy())
    store_logs(parsed_logs)
    alerts = define_alerts(parsed_logs.copy())
    if not alerts.empty:
        print("*Security Alert!*")
        print(alerts)

if __name__ == "__main__":
    main()
