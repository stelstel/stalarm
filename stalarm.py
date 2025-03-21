# stalarm.py
# Author: Stefan Elmgren
# Date: 2021-09-30
# Description: A simple stock alarm program that reads stock data from Yahoo Finance and compares the opening value with the last value. 
#   If the percentage change exceeds a certain limit, the program displays a warning.

import yfinance as yahooFinance
import os
import configparser
import pandas as pd

os.system('cls')

def read_config_ini():
    """
    Reads configuration data from a .ini file, extracting stock symbols and an alarm limit.
    
    The function loads a configuration file (`config.ini`), retrieves stock symbols as a list, 
    and converts the alarm limit into a float.

    Returns:
        symbols (list): A list of stock symbols (e.g., ["META", "AMZN"]).
        alarm_limit (float): The alarm limit value, converted to float (e.g., 2.50).
    """

    # Load the config file
    config = configparser.ConfigParser()
    config.read("config.ini")

    # Read stock symbols
    symbols = config["stocks"]["symbols"].split(", ")  # Converts to a list

    # Read alarm limit as float
    alarm_limit = float(config["settings"]["alarm_limit"])

    return symbols, alarm_limit


symbols, alarm_limit = read_config_ini()

stock_data = []

for symbol in symbols:
    stock_info = yahooFinance.Ticker(symbol)
    company_name = stock_info.info.get("longName", "N/A")
    latest_data = stock_info.history(period="1d")
    opening_value = latest_data["Open"].iloc[-1] # -1 means "the last row" in the DataFrame
    last_value = stock_info.fast_info["last_price"]
    percentage_value_change = ((last_value - opening_value) / opening_value) * 100

    warning = False

    if abs(percentage_value_change) > alarm_limit and percentage_value_change < 0:
        warning = True

    stock_data.append({
        "Symbol": symbol,
        "Company name": company_name,
        "Opening value": opening_value,
        "last value": last_value,
        "Change": percentage_value_change,
        "Warning": warning
    })

# Create a DataFrame with the collected data
df_stock_data = pd.DataFrame(stock_data)

# Display the DataFrame
print(df_stock_data.to_string(index=False))