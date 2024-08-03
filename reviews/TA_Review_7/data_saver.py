# Import api connection details.
from credentials import KEY, SECRET

# Import alpaca trade api.
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.requests import StockLatestQuoteRequest
from alpaca.data.enums import Adjustment
from alpaca.data.timeframe import TimeFrame

import sqlalchemy
import pandas as pd
import pytz
from datetime import datetime, timedelta


client = StockHistoricalDataClient(KEY, SECRET)
    
def get_historical_data(symbols, start, end):
    # Gets historical data from Alpaca
    request_params = StockBarsRequest(
                        symbol_or_symbols=symbols,
                        timeframe=TimeFrame.Minute,
                        start=start,
                        end=end,
                        adjustment=Adjustment.ALL)
    bars = client.get_stock_bars(request_params).df.reset_index()
    return bars

def get_latest_quote(symbols):
    request_params = StockLatestQuoteRequest(symbol_or_symbols=symbols)
    latest_quote = client.get_stock_latest_quote(request_params)
    return latest_quote

def insert_data_frame(data, engine):
    # Save the data to my database
    data.to_sql('market_data', engine, if_exists='append', index=False)

def get_latest_timestamp(engine):
    query = "SELECT MAX(timestamp) FROM market_data"
    result = pd.read_sql(query, engine)
    return result.iloc[0, 0]

def run_data_saver():
    start = datetime(2024, 7, 26)
    end = datetime(2024, 7, 27)
    symbols = ["SPY", "VXX"]
    
    engine = sqlalchemy.create_engine('sqlite:///market_data.db')
    
    try:
        latest_timestamp = get_latest_timestamp(engine)
    except sqlalchemy.exc.OperationalError:
        latest_timestamp = None
    
    if latest_timestamp:
        latest_timestamp = datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S.%f").astimezone(pytz.timezone('UTC'))
        
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        
        # Check that today isn't a weekend
        if datetime.now().weekday() < 5 and latest_timestamp > one_minute_ago:
            # Get historical data
            new_start = latest_timestamp + timedelta(seconds=1)
            new_end = datetime.now()
            new_data = get_historical_data(symbols, new_start, new_end)
            insert_data_frame(new_data, engine)

    else:
        # Get historical data for the initial date range
        data = get_historical_data(symbols, start, end)
        insert_data_frame(data, engine)
        
run_data_saver()