# Import api connection details.
from credentials import KEY, SECRET

# Import alpaca trade api.
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.historical import StockHistoricalDataClient

client = StockHistoricalDataClient(KEY, SECRET)

# Define the function to get historical data
def get_last_quote():
    symbols = ["SPY", "VXX"]

    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
    latest_quote = client.get_stock_latest_quote(request_params)
    print(latest_quote)
    return latest_quote

get_last_quote()

# 1. Getting historical data from alpaca
# 2. Updating that historical from with some frequency
# 3. Saving/making the historical data easily available for backtesting
# 4. Cleaning, etc.

# Extract -> Transform -> Load (ETL)
# Extracting data from somewhere
# Transforming the data to make it look like what you want
# Loading the data into a database/"data lake" <- clean "pool" of data