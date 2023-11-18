


# import zrd_login as zl
import requests
import zrd_login_sridharan as zl
from kiteconnect import KiteConnect
import os
from datetime import datetime, timedelta
import datetime as dt
import pandas as pd
import time
import sys
import pdb
import pytz
from functions.db_conn import sqlalchemy_connect

sql=sqlalchemy_connect(username="chetan")

tables_dict=sql.read_config()

db_tables=tables_dict["db_tables"]

dbs_tickers_data_tbl=db_tables["dbs_tickers_data_table"]
customer_tbl=db_tables["customer_table"]
user_table=db_tables["user_table"]



# cwd = os.chdir("C:\\PythonL")
ohlc_intraday = {}

tickers = ['NIFTY BANK', 'NIFTY 50']
kite = zl.kite

def round_dt(dt1, delta):
    return datetime.min + round((dt1 - datetime.min) / delta) * delta
    # return dt.datetime.min + round((dt1 - datetime.min) / delta) * delta

delta = timedelta(minutes=1)
# pdb.set_trace()
# df = pd.read_csv('trade_listf.csv', index_col=0)
# df['time'] = pd.to_datetime(df['time']) # making it into a time object
# df1 =df.loc[df['action'] == 'Buy']
# print(df1)

# if not df1.empty:
#     ce_name_b = df1.iloc[0]["CE_name"]
#     pe_name_b = df1.iloc[0]["PE_name"]

# tickers = [ce_name_b, pe_name_b]
# tickers =['BANKNIFTY22APR35900CE', 'BANKNIFTY22APR35900PE']
#tickers = ['NIFTY BANK', 'NIFTY 50']
#tickers = ['NIFTY BANK']
df = pd.read_csv('F:/project-12/double_bottom_strategy/scratch/trial/my_dict.csv', index_col=0)
tickers = df.iloc[:, 0]
print("tickers",tickers)
# df_master = pd.read_csv("Chart_input.csv") # Master Template
# # df_master = df_master.loc[:,~df.columns.str.match("Unnamed")]
# column_values1 = df_master["Symbol Name"].values
# watchlist1 = column_values1.tolist()
# tickers = column_values1.tolist()
# pdb.set_trace()



def fetchOHLCExtended(name,inception_date, interval):
    """extracts historical data and outputs in the form of dataframe
       inception date string format - dd-mm-yyyy""" 
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
            #data = data.append(pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval)),ignore_index=True) #Pandas old version append works & Pandas new version concat works
            data = pd.concat([data, pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval))], ignore_index=True)
            break
        else:
            to_date = from_date + dt.timedelta(duration)
            #data = data.append(pd.DataFrame(kite.historical_data(instrument,from_date,to_date,interval)),ignore_index=True) #Pandas old version append works & Pandas new version concat works
            data = pd.concat([data, pd.DataFrame(kite.historical_data(instrument,from_date,dt.date.today(),interval))], ignore_index=True)
            from_date = to_date
    data.set_index("date",inplace=True)
    return data


url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)

df = pd.read_csv("F:/project-12/double_bottom_strategy/scratch/trial/my_dict.csv")[['stock_id','trigger_prices','percentage_change']]
tickers = df.iloc[:, 0]
print(tickers)
df['TakeProfit'] = df['trigger_prices'] * 1.05

print(df)
for i in tickers:
    start = time.time()
    try:
        time.sleep(2)
        ohlc_intraday[i] = fetchOHLCExtended( i,"01-01-2023", "day")
        # ohlc_intraday[i] = fetchOHLCExtended( i,"15-06-2023", "minute")
        #ohlc_intraday[i] = fetchOHLCExtended( i,"01-07-2023", "30minute")
        #ohlc_intraday[i].to_csv(i + '.csv')


        # Extract the last three rows from the CSV file
        last_three_rows = ohlc_intraday[i].tail(3)

        # Find the minimum value from the desired column in the last three rows
        min_value = last_three_rows['low'].min()
        min_value = min_value*99.85/100
        
        # Assign the minimum value to the corresponding stock ID in the dataframe
        df.loc[df['stock_id'] == i, 'Stop Loss'] = min_value

        # Get the value from the 'high' column of the last row
        last_high_value = ohlc_intraday[i]['high'].iloc[-1]
        
        # Assign the last high value to the corresponding stock ID in the dataframe
        df.loc[df['stock_id'] == i, 'Last High'] = last_high_value


    except Exception as e:
        print(e)

    end = time.time()
    print(end - start) #     <-----NOTE Hashed
    print(i,"done") #       <-----NOTE Hashed

current_time=datetime.now()
df.insert(0,'datetime',current_time)

df["stock_id"] = df["stock_id"] + "-EQ"
print(df)

for i in range(len(df)):
    # Find the matching token value in the second dataframe based on stock_id
    token_value = token_df[token_df['symbol'] == df.at[i, 'stock_id']]['token'].values[0]
    
    # Assign the token value to the corresponding row in the first dataframe
    df.at[i, 'trade_token'] = token_value
    
print(df)    

sql.upload_to_table(df,table_name=dbs_tickers_data_tbl,if_exists="append")

"""
time_check = dt.time(9,47)
time_check = dt.time(15,29)
time_now = dt.datetime.now()
# time_now = dt.datetime.now((pytz.timezone('Asia/Kolkata')))
dt1 = time_now
time_check = round_dt(dt1,delta)
now_aware = time_check.replace(tzinfo=pytz.timezone(('Asia/Kolkata')))
tickers_v=[]
tickers_check=[]

print("Checking baseline time now , is the latest candle equal or greater than this time ---> ", now_aware)
# pdb.set_trace()

print("done")
"""
# while True:   
#     for i in tickers:
#         if len(tickers_v) == 1:
#         # if len(tickers_v) == 2:
#             break
#         if os.path.isfile(i + '.csv'):
#             df = pd.read_csv(i + '.csv')
#             df['date'] = pd.to_datetime(df['date'])
#             # df['expiry'] = pd.to_datetime(df['expiry'])
#             # starttime = pd.to_datetime("2022-03-24 09:46:00+05:30").time()
#             time_now = dt.datetime.now().time().replace(microsecond=0)
#             # starttime = pd.to_datetime(df.iloc[-1]['date']).time() # https://stackoverflow.com/questions/49554491/not-supported-between-instances-of-datetime-date-and-str
#             starttime = (df.iloc[-1]['date'])
#             # validate = starttime >=time_check
#             str1 = str(starttime)
#             datetime_obj = dt.datetime.strptime(str1,"%Y-%m-%d %H:%M:%S+05:30")
#             datetime_obj =  datetime_obj.replace(tzinfo=pytz.timezone(('Asia/Kolkata')))
#             # datetime_obj > now_aware
            
#             validate = datetime_obj >= now_aware # Validate Previous candle is formed
#             # validate = datetime_obj <= now_aware # Validate Previous candle is formed # For TESTING ONLY ---> Remember to HASH this line
#             # pdb.set_trace()
            

#             if validate:
#                 tickers_check=[i]
#                 tickers_v += tickers_check
#                 tickers_v = list(set(tickers_v)) # https://stackoverflow.com/questions/66952798/how-do-i-update-a-list-using-the-for-loop
#                 print(tickers_v)
#                 time.sleep(2)
#                 # if len(tickers_v) == 2:
#                 if len(tickers_v) == 1:
#                     # sys.exit()
#                     print("COMPLETED downloading both tickers --->", tickers_v)
#                     # break                
#             else:
#                 try:
#                     #ohlc_intraday[i] = fetchOHLCExtended( i,"01-07-2023", "30minute")
#                     ohlc_intraday[i] = fetchOHLCExtended( i,"01-01-2021", "day")
#                     ohlc_intraday[i].to_csv(i + '.csv')
#                     print(time_now)
#                     print("downloaded the get_data file for ticker again--->" , i)
#                     print("\n")
#                     print("latest candle 1 min downloaded time stamp is ----> ", datetime_obj)
#                     print("Validate , is the latest candle time stamp equal or greater than this time ---> ", now_aware)
#                     time.sleep(2)
#                 except Exception as e:
#                     print(e)
#     if len(tickers_v) == 1:
#         break




