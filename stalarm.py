# stalarm.py
# Author: Stefan Elmgren
# Date: 2025-03-21
# Description: A simple stock alarm program that reads stock data from Yahoo Finance and compares the opening value with the last value. 
#   If the percentage change exceeds a certain limit, the program displays a warning.

import yfinance as yahooFinance
import os
import configparser
import pandas as pd

# Clear console
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
    config_file = "config.ini"
    config.read(config_file)

    # Read stock symbols
    stock_symbols = config["stocks"]["symbols"].replace(" ", "")  # Removes spaces
    symbols = stock_symbols.split(",")  # Converts to a list

    # Read alarm limit as float
    alarm_limit = float(config["settings"]["alarm_limit"])

    return symbols, alarm_limit


# Read configuration
symbols, alarm_limit = read_config_ini()

# List to store stock data
stock_data = []

for symbol in symbols:
    try:
        stock_info = yahooFinance.Ticker(symbol)

        # Fetch stock data
        stock_data_dict = stock_info.get_info()
        if not stock_data_dict:
            raise ValueError(f"No data available for {symbol}")

        company_name = stock_data_dict.get("longName", "N/A")

        # Get historical data
        latest_data = stock_info.history(period="1d")
        if latest_data.empty:
            raise ValueError(f"No historical data available for {symbol}")

        opening_value = latest_data["Open"].iloc[-1]  # Last available opening price
        last_value = stock_info.fast_info["last_price"]
        percentage_value_change = ((last_value - opening_value) / opening_value) * 100

        warning = abs(percentage_value_change) > alarm_limit and percentage_value_change < 0

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        company_name = "N/A"
        opening_value = "N/A"
        last_value = "N/A"
        percentage_value_change = "N/A"
        warning = False

    stock_data.append({
        "Symbol": symbol,
        "Company name": company_name,
        "Opening value": opening_value,
        "Last value": last_value,
        "Change %": percentage_value_change,
        "Warning": warning
    })

# Create a DataFrame with the collected data
df_stock_data = pd.DataFrame(stock_data)

# Display the DataFrame
print(df_stock_data.to_string(index=False))
