# stalarm.py
# Author: Stefan Elmgren
# Date: 2025-03-21 - 2025-03-24
# Description: A simple stock alarm program that reads stock data from Yahoo Finance and compares the opening value with the last value. 
#   If the percentage change exceeds a certain limit, the program displays a warning.

import yfinance as yahooFinance
import os
import configparser
import pandas as pd
import pytz

# TODO add update_frequency to config.ini

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

    # Read limits as floats
    alarm_limit_decrease = float(config["settings"]["alarm_limit_decrease"])
    alarm_limit_raise_after_decrease = float(config["settings"]["alarm_limit_raise_after_decrease"])

    # Read start date as date
    start_date = config["settings"]["start-date"]

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



# Read configuration
symbols, alarm_limit_decrease, alarm_limit_raise_after_decrease, start_date = read_config_ini()

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

        # Get historical data since start date
        historical_data = stock_info.history(start=start_date)

        if historical_data.empty:
            raise ValueError(f"No historical data available for {symbol} since {start_date}")
        
        if start_date in historical_data.index:
            # Define Swedish time zone
            # swedish_timezone = pytz.timezone('Europe/Stockholm')

            # Get the opening value for the specific date (start_date)
            opening_value_historic = float(historical_data.loc[start_date, "Open"])

            # Get the lowest price in historical data
            lowest_price_historical = float(historical_data["Low"].min())

            # Get the date and time of the lowest price
            lowest_price_time = historical_data["Low"].idxmin()

            # If the index (date) is not timezone-aware, localize it to UTC
            if lowest_price_time.tzinfo is None:
                lowest_price_time = pytz.utc.localize(lowest_price_time)

            # Convert the timestamp to Swedish time zone (CET/CEST)
            #lowest_price_time_swedish = convert_to_swedish_timezone(lowest_price_time)

            # Get the highest price in historical data
            highest_price_historical = float(historical_data["High"].max())

            # Get the date and time of the highest price
            highest_price_time = historical_data["High"].idxmax()

            # If the index (date) is not timezone-aware, localize it to UTC
            if highest_price_time.tzinfo is None:
                highest_price_time = pytz.utc.localize(highest_price_time)

            # Convert the timestamp to Swedish time zone (CET/CEST)
            #highest_price_time_swedish = convert_to_swedish_timezone(highest_price_time)

            if(lowest_price_historical < opening_value_historic and ( (opening_value_historic - lowest_price_historical) * 100 > alarm_limit_decrease) ):
                print(f"Lowest price {lowest_price_historical} is lower than opening value {opening_value_historic}")

        else:
            raise ValueError(f"No data available for {start_date}")
        
    except Exception as e:
        msg_to_user = f"Error fetching data for {symbol}, Is this symbol correct? Check at https://finance.yahoo.com/lookup/"
        print(f"Error fetching data for {symbol}: {e}") #/////////////////////////////////////////////////////////////
        company_name = "N/A"
        warning = False

    stock_data.append({
        "Symbol": symbol,
        "Company name": company_name,
        "Opening value": opening_value_historic,
        "Lowest price": lowest_price_historical,
        "Lowest price time": lowest_price_time_swedish,
        "Highest price": highest_price_historical,
        "Highest price time": highest_price_time_swedish
    })

# Create a DataFrame with the collected data
df_stock_data = pd.DataFrame(stock_data)

# Display the DataFrame
print(df_stock_data.to_string(index=False))
