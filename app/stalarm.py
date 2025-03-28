# stalarm.py
# Author: Stefan Elmgren
# Date: 2025-03-21 - 2025-03-25

# Description: A simple stock alarm program that checks if the stock price goes down beyond
#   a specified decrease limit, then rises again after hitting that low. 
#   Alerts are triggered based on this behavior using data fetched from Yahoo Finance.

import yfinance as yahooFinance
import os
import pandas as pd
import pytz

from functions import read_config_ini, convert_to_swedish_timezone

# TODO add update_frequency to config.ini etc.
# TODO Expand msg_to_user
# TODO historic, historical

# Clear console
os.system('cls')

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
        
        # If start_date is missing, find the closest next available date
        if start_date not in historical_data.index:
            closest_dates = historical_data.index[historical_data.index > start_date]  # Find future dates

            if not closest_dates.empty:
                start_date = closest_dates[0]  # Use the first available future date
            else:
                start_date = historical_data.index[-1]  # Fallback to the latest available date

        if start_date in historical_data.index:
            # Get the opening value for the specific date (start_date)
            opening_value_historic = float(historical_data.loc[start_date, "Open"])

            # Filter historical data to only include prices from the start date onward
            historical_data_filtered = historical_data.loc[start_date:]

            # Get the lowest price within the filtered historical data
            lowest_price_historical = float(historical_data_filtered["Low"].min())

            # Get the date and time of the lowest price (within the filtered range)
            lowest_price_time = historical_data_filtered["Low"].idxmin()

            # If the index (date) is not timezone-aware, localize it to UTC
            if lowest_price_time.tzinfo is None:
                lowest_price_time = pytz.utc.localize(lowest_price_time)

            # Convert the timestamp to Swedish time zone (CET/CEST)
            lowest_price_time_swedish = convert_to_swedish_timezone(lowest_price_time)

            # Get the highest price within the filtered historical data
            highest_price_historical = float(historical_data_filtered["High"].max())

            # Get the date and time of the highest price (within the filtered range)
            highest_price_time = historical_data_filtered["High"].idxmax()

            # Get the latest available price
            latest_price = float(stock_info.fast_info["last_price"])

            # Get the date and time of the latest price (within the filtered range)
            latest_price_time = historical_data_filtered["Close"].idxmax()

            # If the index (date) is not timezone-aware, localize it to UTC
            if highest_price_time.tzinfo is None:
                highest_price_time = pytz.utc.localize(highest_price_time)

            # Convert the timestamp to Swedish time zone (CET/CEST)
            highest_price_time_swedish = convert_to_swedish_timezone(highest_price_time)

            decrease_limit_reached = False

            if (lowest_price_historical < opening_value_historic and ( ( (opening_value_historic - lowest_price_historical) / 100) / opening_value_historic) * 100 > alarm_limit_decrease / 100):
                decrease_limit_reached = True

            raise_limit_reached_after_decrease_limit_reached = False

            if(latest_price > lowest_price_historical * (1 + alarm_limit_raise_after_decrease / 100) and lowest_price_time < latest_price_time and decrease_limit_reached):    
                raise_limit_reached_after_decrease_limit_reached = True
        else:
            raise ValueError(f"No data available for {symbol} on {start_date}, latest available is {historical_data.index[-1]}")
        
    except Exception as e:
        msg_to_user = f"Error fetching data for {symbol}, Is this symbol correct? Check at https://finance.yahoo.com/lookup/"
        print(f"Error fetching data for {symbol}: {e}") #/////////////////////////////////////////////////////////////
        company_name = start_date, opening_value_historic = lowest_price_historical = lowest_price_time_swedish = highest_price_historical = highest_price_time_swedish = decrease_limit_reached = raise_limit_reached_after_decrease_limit_reached = "N/A"

    stock_data.append({
        "Actual start date": start_date,
        "Symbol": symbol,
        "Company name": company_name,
        "Opening value": opening_value_historic,
        "Lowest price": lowest_price_historical,
        "Lowest price time": lowest_price_time_swedish,
        "Highest price": highest_price_historical,
        "Highest price time": highest_price_time_swedish,
        "Latest price": latest_price,
        "Latest price time": latest_price_time,
        f"Decrease limit reached({alarm_limit_decrease} %)": decrease_limit_reached,
        f"Raise limit reached after decrease limit reached({alarm_limit_raise_after_decrease} %)":  raise_limit_reached_after_decrease_limit_reached
    })

# Create a DataFrame with the collected data
df_stock_data = pd.DataFrame(stock_data)

# Display the DataFrame
print(df_stock_data.to_string(index=False))