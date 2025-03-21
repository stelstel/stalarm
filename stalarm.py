import yfinance as yahooFinance
import os
import configparser
import pandas as pd

os.system('cls')

def read_config_ini():
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
    print(symbol)
    company_name = stock_info.info.get("longName", "N/A")
    print(company_name)
    latest_data = stock_info.history(period="1d")
    print(latest_data["Open"].iloc[-1]) # -1 means "the last row" in the DataFrame
    opening_value = latest_data["Open"].iloc[-1] # -1 means "the last row" in the DataFrame
    last_value = stock_info.fast_info["last_price"]
    print(stock_info.fast_info["last_price"])  # Latest stock price

    stock_data.append({
        "symbol": symbol,
        "company_name": company_name,
        "opening_value": opening_value,
        "last_value": last_value
    })

# Create a DataFrame with the collected data
df_stock_data = pd.DataFrame(stock_data)

# Display the DataFrame
print(df_stock_data)

# print(symbols)      # ['META', 'AMZN', 'AAPL', 'TSLA']
# print(alarm_limit)  # 2.50

# # Here We are getting Facebook financial information
# # We need to pass FB as argument for that
# GetFacebookInformation = yahooFinance.Ticker("META")
 
# # whole python dictionary is printed here
# # print(GetFacebookInformation.info)
# #print(GetFacebookInformation.history(period="1d"))

# latest_data = GetFacebookInformation.history(period="1d")

# print(latest_data["Open"].iloc[-1]) # -1 means "the last row" in the DataFrame

# print(GetFacebookInformation.fast_info["last_price"])  # Latest stock price