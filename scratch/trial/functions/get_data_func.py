import os
from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import time
import sys
import pdb
import pytz


def live_zone_time():
    """
        Retrive the current live time of native zone, with rouduo value
    """
    time_now = dt.datetime.now() + timedelta(hours=5,minutes=30)
    #time_now = dt.datetime.now()
    dt1 = time_now
    delta = timedelta(minutes=1)
    time_check=datetime.min + round((dt1 - datetime.min) / delta) * delta
    now_aware = time_check.replace(tzinfo=pytz.timezone(('Asia/Kolkata')))
    return now_aware

def fetchOHLCExtended(kite,name,inception_date, interval):

    """
        extracts historical data and outputs in the form of dataframe
        inception date string format - dd-mm-yyyy
    """ 
    if interval == "minute":
        duration = 60
    elif interval == "3minute" or interval == "5minute" or interval == "10minute":
        duration = 100
    elif interval == "15minute" or interval == "30minute":
        duration = 200   
    elif interval == "60minute":
        duration = 400
    elif interval == "day":
        duration = 2000    
    
    zrd_name = 'NSE:' + name
    # zrd_name = 'NFO:' + name
    
    instrument = kite.ltp(zrd_name)[zrd_name]['instrument_token']
    from_date = dt.datetime.strptime(inception_date, '%d-%m-%Y')
    to_date = dt.date.today()
    data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    while True:
        if from_date.date() >= (dt.date.today() - dt.timedelta(duration)):
            #data = data.append(pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval)),ignore_index=True)
            data = pd.concat([data, pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval))], ignore_index=True)
            break
        else:
            to_date = from_date + dt.timedelta(duration)
            #data = data.append(pd.DataFrame(kite.historical_data(instrument,from_date,to_date,interval)),ignore_index=True)
            data = pd.concat([data, pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval))], ignore_index=True)
            from_date = to_date
    #data.set_index("date",inplace=True)
    return data