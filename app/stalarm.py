# stalarm.py
# Author: Stefan Elmgren
# Date: 2025-03-21 - 2025-03-31

# Description: A simple stock alarm program that checks if the stock price goes down beyond
#   a specified decrease limit, then rises again after hitting that low. 
#   Alerts are triggered based on this behavior using data fetched from Yahoo Finance.

# TODO add update_frequency
# TODO Expand msg_to_user
# TODO Every stock should have their own inc_limit, dec_limit, and start_date ???
# TODO Remove every second row different color

""""
    import yfinance as yahooFinance
    import os
    import pandas as pd
    import pytz

    from functions import read_config_ini, custom_sort, convert_to_swedish_timezone

    # Clear console
    os.system('cls')

    start_time_swedish = "N/A"

    # Read configuration
    symbols, alarm_limit_decrease, alarm_limit_increase_after_decrease, start_date, price_decimals = read_config_ini()

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
                # Convert the timestamp to Swedish time zone (CET/CEST)
                start_time_swedish = convert_to_swedish_timezone(start_date)

                # Get the opening value for the specific date (start_date)
                opening_price_historical = float(historical_data.loc[start_date, "Open"])

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

                # If the index (date) is not timezone-aware, localize it to UTC
                if highest_price_time.tzinfo is None:
                    highest_price_time = pytz.utc.localize(highest_price_time)

                # Convert the timestamp to Swedish time zone (CET/CEST)
                highest_price_time_swedish = convert_to_swedish_timezone(highest_price_time)

                # Get the latest available price
                latest_price = float(stock_info.fast_info["last_price"])

                # Get the date and time of the latest price (current time in Swedish timezone)
                latest_price_time = pd.Timestamp.now(pytz.timezone('Europe/Stockholm'))

                # Convert the latest price time to Swedish time
                latest_price_time_swedish = convert_to_swedish_timezone(latest_price_time)

                decrease_limit_reached = False

                if (lowest_price_historical < opening_price_historical and ( ( (opening_price_historical - lowest_price_historical) / 100) / opening_price_historical) * 100 > alarm_limit_decrease / 100):
                    decrease_limit_reached = True

                increase_limit_reached_after_decrease_limit_reached = False

                # if(latest_price > lowest_price_historical * (1 + alarm_limit_increase_after_decrease / 100) and lowest_price_time < latest_price_time and decrease_limit_reached):
                if(latest_price > lowest_price_historical * (1 + alarm_limit_increase_after_decrease / 100) and decrease_limit_reached):    
                    increase_limit_reached_after_decrease_limit_reached = True
            else:
                raise ValueError(f"No data available for {symbol} on {start_date}, latest available is {historical_data.index[-1]}")

        except Exception as e:
            msg_to_user = f"Error fetching data for {symbol}, Is this symbol correct? Check at https://finance.yahoo.com/lookup/"
            # company_name = start_date, opening_price_historical = lowest_price_historical = lowest_price_time_swedish = highest_price_historical = highest_price_time_swedish = decrease_limit_reached = increase_limit_reached_after_decrease_limit_reached = "N/A"
            company_name = "N/A"
            start_date = "N/A"
            opening_price_historical = 0.0
            lowest_price_historical = 0.0
            highest_price_historical = 0.0
            highest_price_time_swedish = None
            decrease_limit_reached = False
            increase_limit_reached_after_decrease_limit_reached = False
            start_time_swedish = None
            lowest_price_time_swedish = None
            latest_price = 0.0
            latest_price_time_swedish = None

        stock_data.append({
            "Company name": company_name,
            "Symbol": symbol,
            "Actual start date": start_time_swedish,
            "Opening price": round(opening_price_historical, price_decimals),
            "Lowest price": round(lowest_price_historical, price_decimals),
            "Lowest price time": lowest_price_time_swedish,
            "Highest price": round(highest_price_historical, price_decimals),
            "Highest price time": highest_price_time_swedish,
            "Latest price": round(latest_price, price_decimals),
            "Latest price time": latest_price_time_swedish,
            "Dec. lim. reached": decrease_limit_reached,
            "Dec. lim.": f"{alarm_limit_decrease} %",
            "Inc. lim. reached after dec. lim. reached":  increase_limit_reached_after_decrease_limit_reached,
            "Inc. lim.": f"{alarm_limit_increase_after_decrease} %"
        })

    # Create a DataFrame with the collected data
    df_stock_data = pd.DataFrame(stock_data)

    # Sorting the DataFrame based on the custom sort function
    df_stock_data = custom_sort(df_stock_data)

    # Display the DataFrame
    print(df_stock_data.to_string(index=False)) # ////////////////////////////////////////////////////////
"""

import os
import pandas as pd
import pytz
import requests
from datetime import datetime
from functions import read_config_ini, custom_sort, convert_to_swedish_timezone

# Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "B2YO4YKTC19IXMTG"
BASE_URL = "https://www.alphavantage.co/query"

# Clear console
os.system('cls')

# Read configuration
symbols, alarm_limit_decrease, alarm_limit_increase_after_decrease, start_date, price_decimals = read_config_ini()

# List to store stock data
stock_data = []

def fetch_stock_data(symbol):
    url = f"{BASE_URL}?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        raise ValueError(f"No data available for {symbol}")
    return data["Time Series (Daily)"]

for symbol in symbols:
    try:
        historical_data = fetch_stock_data(symbol)
        df = pd.DataFrame.from_dict(historical_data, orient='index')
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        if start_date not in df.index:
            future_dates = df.index[df.index > pd.to_datetime(start_date)]
            start_date = future_dates[0] if not future_dates.empty else df.index[-1]

        start_time_swedish = convert_to_swedish_timezone(start_date)
        opening_price_historical = float(df.loc[start_date, "1. open"])
        lowest_price_historical = float(df.loc[start_date:, "3. low"].min())
        highest_price_historical = float(df.loc[start_date:, "2. high"].max())
        latest_price = float(df.iloc[-1]["4. close"])

        lowest_price_time = df.loc[start_date:, "3. low"].idxmin()
        highest_price_time = df.loc[start_date:, "2. high"].idxmax()
        latest_price_time = df.index[-1]

        lowest_price_time_swedish = convert_to_swedish_timezone(lowest_price_time)
        highest_price_time_swedish = convert_to_swedish_timezone(highest_price_time)
        latest_price_time_swedish = convert_to_swedish_timezone(latest_price_time)

        decrease_limit_reached = False

        decrease_limit_reached = (lowest_price_historical < opening_price_historical and
                                  ((opening_price_historical - lowest_price_historical) / opening_price_historical) * 100 > alarm_limit_decrease)
        
        increase_limit_reached_after_decrease = False
        
        increase_limit_reached_after_decrease = (latest_price > lowest_price_historical * (1 + alarm_limit_increase_after_decrease / 100) and
                                                 decrease_limit_reached)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        continue

    stock_data.append({
        "Symbol": symbol,
        "Actual start date": start_time_swedish,
        "Opening price": round(opening_price_historical, price_decimals),
        "Lowest price": round(lowest_price_historical, price_decimals),
        "Lowest price time": lowest_price_time_swedish,
        "Highest price": round(highest_price_historical, price_decimals),
        "Highest price time": highest_price_time_swedish,
        "Latest price": round(latest_price, price_decimals),
        "Latest price time": latest_price_time_swedish,
        "Dec. lim. reached": decrease_limit_reached,
        "Dec. lim.": f"{alarm_limit_decrease} %",
        "Inc. lim. reached after dec. lim.": increase_limit_reached_after_decrease,
        "Inc. lim.": f"{alarm_limit_increase_after_decrease} %"
    })

# Create a DataFrame
df_stock_data = pd.DataFrame(stock_data)
df_stock_data = custom_sort(df_stock_data)
print(df_stock_data.to_string(index=False))

