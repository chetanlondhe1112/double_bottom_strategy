
#import zrd_login as zl
import datetime as dt
import yfinance as yf
import time
import json
import pandas as pd
import requests
import pdb
import os
from bs4 import BeautifulSoup
import warnings
from SmartApi.smartConnect import SmartConnect
import datetime
import time
import mibian
import pyotp
import sys
from functions.db_conn import sqlalchemy_connect


sql=sqlalchemy_connect(username="chetan")

tables_dict=sql.read_config()

db_tables=tables_dict["db_tables"]
tickers_data_tbl=db_tables["tickers_data_table"]


countt = 0

# def get_stocks():
#kite = zl.kite
print("waiting to start scan at 3:27pm")
"""
while True:
    time_now = dt.datetime.now().time().replace(microsecond=0)
    print(time_now)
    time.sleep(5)
    if time_now>=datetime.time(15,27,00):
        print("The Time is 15:27")
        break
"""
with requests.Session() as s:
    scanner_url = 'https://chartink.com/screener/copy-daily-double-bottom-1143' 
    
    r = s.get(scanner_url)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.select_one("[name='csrf-token']")['content']
    s.headers['x-csrf-token'] = csrf
    process_url = 'https://chartink.com/screener/process'    
    payload = {
        'scan_clause':
        #'( {33492} ( latest close > latest sma( latest close , 200 ) and latest close > latest sma( latest close , 50 ) and latest close > latest sma( latest close , 10 ) and latest close > latest ichimoku cloud top( 9 , 26 , 52 ) and latest close > latest supertrend( 7 , 3 ) and latest adx( 14 ) > 25 and latest adx di positive( 14 ) > 20 and latest rsi( 14 ) > 50 ) )'
        '( {33492} ( latest sma ( volume,20 ) * latest close >= 44000000 and ( {cash} ( ( {cash} ( abs ( 15 days ago min ( 45 , latest low ) - latest min ( 3 , latest low ) ) <= latest min ( 3 , latest open ) * 0.03 ) ) ) ) and latest close > latest open ) )'

    }             

    r = s.post(process_url, data=payload)
    df = r.json()
    df = pd.DataFrame(df)
    stocks = []
    # pdb.set_trace()
    trigger_prices = []
    percentage_change=[]


    for i in range(len(df['data'])):
        stocks.append(df['data'][i]['nsecode'])
        trigger_prices.append(df['data'][i]['close'])
        percentage_change.append(df['data'][i]['per_chg'])
    my_dict = {'stock_id':[],"trigger_prices":[],"percentage_change":[]}
    
    for i in range(len(stocks)):   
        my_dict["stock_id"].append(stocks[i])
        my_dict['trigger_prices'].append(trigger_prices[i])
        my_dict['percentage_change'].append(percentage_change[i])
        xn = len(stocks)

        
time_now = dt.datetime.now().time().replace(microsecond=0)
today_date = dt.date.today()
date = today_date.strftime("%d %B, %Y")

print("\n")

print("======================================================= ")
print("stocks selected from Rishi John Issac's Bullish Scan on  ",date, " ", time_now)
print("======================================================= ")
print("Filter condition as per url --------------> https://chartink.com/screener/bullish-stocks-24083527")
print("number of stocks selected from scan ------> ", xn)

print("\n")
watchlist = my_dict['stock_id']
print("<------- The list of stocks selected from scan -------> ")
print(watchlist)
# print(my_dict)
print("\n")


# Convert dictionary to DataFrame
df = pd.DataFrame(my_dict)

df.to_csv('my_dict.csv')


#df = pd.read_csv('my_dict.csv', index_col=0)
os.system('python F:/project-12/double_bottom_strategy/scratch/trial/get_data_day.py')

"""
# Calculate take profit
df['TakeProfit'] = df['trigger_prices'] * 1.05

# Specify the folder path where the CSV files are located
folder_path = "F:/project-12/double_bottom_strategy/scratch/trial"

# Iterate over each stock ID in the dataframe
for stock_id in df['stock_id']:
    # Construct the full path to the CSV file for the current stock ID
    csv_file_path = os.path.join(folder_path, f"{stock_id}.csv")
    
    # Read the CSV file for the current stock ID
    csv_data = pd.read_csv(csv_file_path)

    # Extract the last three rows from the CSV file
    last_three_rows = csv_data.tail(3)

    # Find the minimum value from the desired column in the last three rows
    min_value = last_three_rows['low'].min()
    min_value = min_value*99.85/100
    
    # Assign the minimum value to the corresponding stock ID in the dataframe
    df.loc[df['stock_id'] == stock_id, 'Stop Loss'] = min_value

    # Get the value from the 'high' column of the last row
    last_high_value = csv_data['high'].iloc[-1]
    
    # Assign the last high value to the corresponding stock ID in the dataframe
    df.loc[df['stock_id'] == stock_id, 'Last High'] = last_high_value

print(df)
sql.upload_to_table(df,table_name=tickers_data_tbl,if_exists="replace")
"""