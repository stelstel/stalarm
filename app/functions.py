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

    price_decimals = int(config["settings"]["max_price_decimals"])

    return symbols, alarm_limit_decrease, alarm_limit_raise_after_decrease, start_date, price_decimals


def convert_to_swedish_timezone(time):
    """
    Converts a given timestamp to Swedish time zone (CET/CEST) and removes timezone info.
    
    Args:
        time (datetime): The datetime object to be converted.
        
    Returns:
        str: The formatted datetime string in Swedish time zone without seconds.
    """

    # Define Swedish time zone
    swedish_timezone = pytz.timezone("Europe/Stockholm")

    # If the input datetime is not timezone-aware, assume it's in UTC
    if time.tzinfo is None:
        time = pytz.utc.localize(time)

    # Convert the timestamp to Swedish time zone (CET/CEST)
    time_swedish = time.astimezone(swedish_timezone)

    # Format the datetime as 'YYYY-MM-DD HH:MM' (without seconds)
    return time_swedish.strftime("%Y-%m-%d %H:%M")


def custom_sort(df):
    """
    Sort the DataFrame based on specific conditions:
    1. Rows where raise_limit_reached_after_decrease_limit_reached = True and decrease_limit_reached = True.
    2. Rows where raise_limit_reached_after_decrease_limit_reached = False and decrease_limit_reached = True.
    3. Rows where decrease_limit_reached = False.

    Args:
    df (pd.DataFrame): The DataFrame to be sorted.

    Returns:
    pd.DataFrame: The sorted DataFrame.
    """
    # Create a custom sort key based on the conditions:
    df['custom_sort'] = (
        (df['Inc. lim. reached after decrease lim. reached'] == True) &
        (df['Dec. lim. reached'] == True)
    ).astype(int) * 2 + (
        (df['Inc. lim. reached after decrease lim. reached'] == False) &
        (df['Dec. lim. reached'] == True)
    ).astype(int) * 1

    # Sort the DataFrame based on the custom_sort column
    df_sorted = df.sort_values(by='custom_sort', ascending=False)

    # Drop the custom_sort column as it's no longer needed
    df_sorted = df_sorted.drop(columns='custom_sort')

    return df_sorted