# functions.py
# Author: Stefan Elmgren
# Date: 2025-03-21 - 2025-03-25

import configparser
from datetime import datetime
import pytz

def read_config_ini():
    """
    Loads the stock monitoring configuration from 'config.ini'.
    
    Reads stock symbols, alarm limits, and the start date from the config file and returns them as structured data.

    Returns:
        tuple: A tuple containing:
            - symbols (list): A list of stock symbols.
            - alarm_limit_decrease (float): Percentage decrease that triggers an alarm.
            - alarm_limit_raise_after_decrease (float): Percentage increase after a decrease that triggers an alarm.
            - start_date (datetime): The start date for monitoring stock data.
    """

    # Load the config file
    config = configparser.ConfigParser()
    config_file_path = "app/config"
    config_file = "config.ini"
    config.read(f"{config_file_path}/{config_file}")

    # Read stock symbols
    stock_symbols = config["stocks"]["symbols"].replace(" ", "")  # Removes spaces
    symbols = stock_symbols.split(",")  # Converts to a list

    # Read limits as floats
    alarm_limit_decrease = float(config["settings"]["alarm_limit_decrease"])
    alarm_limit_raise_after_decrease = float(config["settings"]["alarm_limit_raise_after_decrease"])

    # Read start date as a datetime object
    start_date = datetime.strptime(config["settings"]["start_date"], "%Y-%m-%d")

    # Ensure that start_date is in the same timezone as historical_data.index
    sweden_tz = pytz.timezone("Europe/Stockholm")
    start_date = sweden_tz.localize(start_date) if start_date.tzinfo is None else start_date

    return symbols, alarm_limit_decrease, alarm_limit_raise_after_decrease, start_date


def convert_to_swedish_timezone(time):
    """
    Converts a given timestamp to Swedish time zone (CET/CEST).
    
    Args:
        time (datetime): The datetime object to be converted.
        
    Returns:
        datetime: The converted datetime object in Swedish time zone.
    """

    # Define Swedish time zone
    swedish_timezone = pytz.timezone('Europe/Stockholm')
    
    # If the index (date) is not timezone-aware, localize it to UTC
    if time.tzinfo is None:
        time = pytz.utc.localize(time)
    
    # Convert the timestamp to Swedish time zone (CET/CEST)
    return time.astimezone(swedish_timezone)