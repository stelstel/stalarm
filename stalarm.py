import yfinance as yahooFinance
import os

os.system('cls')

# Here We are getting Facebook financial information
# We need to pass FB as argument for that
GetFacebookInformation = yahooFinance.Ticker("META")
 
# whole python dictionary is printed here
# print(GetFacebookInformation.info)
#print(GetFacebookInformation.history(period="1d"))

latest_data = GetFacebookInformation.history(period="1d")

print(latest_data["Open"].iloc[-1]) # -1 means "the last row" in the DataFrame

print(GetFacebookInformation.fast_info["last_price"])  # Latest stock price