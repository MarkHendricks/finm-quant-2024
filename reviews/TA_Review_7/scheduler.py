import schedule 
import time
from data_saver import run_data_saver
from real_time_data import get_last_quote

schedule.every(5).minutes.do(run_data_saver)
# you probably want some rate limiting feature here
schedule.every(3).seconds.do(get_last_quote)

while True:
    schedule.run_pending()
    time.sleep(1)