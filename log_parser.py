import logging
import pandas as pd
import re

def parse_logs(logs_df):
    """Parses logs based on a predefined regular expression (modify as needed).

    Args:
        logs_df (pandas.DataFrame): A DataFrame containing a column named "message"
                                    with the log entries as strings.

    Returns:
        pandas.DataFrame: A DataFrame with parsed log information as separate columns.
    """

    try:
        pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (?P<facility>\w+): (?P<level>\w+): (?P<message>.*)"
        logs_df["timestamp"] = pd.to_datetime(logs_df["message"].str.extract(pattern)["timestamp"])
        logs_df["facility"] = logs_df["message"].str.extract(pattern)["facility"]
        logs_df["level"] = logs_df["message"].str.extract(pattern)["level"]
        logs_df["message"] = logs_df["message"].str.extract(pattern)["message"]
        logs_df = logs_df.drop("message", axis=1)  # Remove original, parsed message column
        return logs_df
    except KeyError:  # Handle cases where pattern doesn't match all groups
        logging.warning("Regular expression failed to match log format. Consider adjusting the pattern.")
        return logs_df  # Return original DataFrame (unparsed)
