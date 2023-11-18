
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

countt = 0

# def get_stocks():
#kite = zl.kite
print("waiting to start scan at 3:27pm")
while True:
    time_now = dt.datetime.now().time().replace(microsecond=0)
    print(time_now)
    time.sleep(5)
    if time_now>=datetime.time(15,27,00):
        print("The Time is 15:27")
        break

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
os.system('get_data_day.py')

# Calculate take profit
df['TakeProfit'] = df['trigger_prices'] * 1.05

# Specify the folder path where the CSV files are located
folder_path = "C:/Users/Administrator/Desktop/Double Bottom Strategy"

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
    
#To find the trade_token for each symbols
"""
df["stock_id"] = df["stock_id"] + "-EQ"
url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)

for i in range(len(df)):
    # Find the matching token value in the second dataframe based on stock_id
    token_value = token_df[token_df['symbol'] == df.at[i, 'stock_id']]['token'].values[0]
    
    # Assign the token value to the corresponding row in the first dataframe
    df.at[i, 'trade_token'] = token_value


print(df)
list1=df['stock_id'].values.tolist()

#client_data = {"Sridharan": "250000", "Praveen": "1000", "Ashok": "500000"}
client_data = {"Sridharan": "100000"}
max_stocks = 4

df = df.copy()  # Assuming you have a master dataframe called 'df'

dfs = {}  # Dictionary to store the separate dataframes for each client

for client, funds in client_data.items():
    per_stock = int(funds) / max_stocks
    df_client = df.copy()
    value, decimal = divmod(per_stock / df_client['trigger_prices'],1) 
    df_client["number_of_stocks"] =  value
    df_client["per_stock_value"]= per_stock
    df_client = df_client.sort_values(by='percentage_change', ascending=False).reset_index(drop=True)
    #df_client = df_client.head(max_stocks)
    df_client['Value_Stock'] = df_client['number_of_stocks'] * df_client['trigger_prices'] 
    #df_client['balance_stocks_to_buy'] = len(df_client)
    df_client['Number_of_Stocks_Balance'] = 0
    dfs[client] = df_client

# Access the separate dataframes for each client
#df_Sridharan = dfs["Sridharan"]
df_Sridharan = dfs["Sridharan"]
#df_Ashok = dfs["Ashok"]
df_Sridharan['Order_Placed']=False
df_Sridharan['SELL_Order_Placed'] = False
#print(df_Sridharan)
print(df_Sridharan)
#print(df_Ashok)
df_Sridharan.to_csv('List_Sridharan_03.csv')
#df_Sridharan.to_csv('List_Sridharan.csv', mode='a', index=True, header=False)

#append the next day stocks to same csv file


# remove if same stock exists if sell_order_placed is false
"""