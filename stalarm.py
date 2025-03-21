import yfinance as yahooFinance
import os
import configparser

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

for symbol in symbols:
    stock_info = yahooFinance.Ticker(symbol)
    print(symbol)
    latest_data = stock_info.history(period="1d")
    print(latest_data["Open"].iloc[-1]) # -1 means "the last row" in the DataFrame
    print(stock_info.fast_info["last_price"])  # Latest stock price

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