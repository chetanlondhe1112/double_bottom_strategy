
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
import datetime as dt


def angelbrok_login():
    try:
        global feed_token, client_code, obj, password, refreshToken, accessToken, data
        
        # countt = 0
        # countt = countt+1
        # apikey = 'rHUQcZsN' 
        # username = 'P52012673'
        # #pwd = 'Pk@123'
        # pwd = '9845'
        # kiteSetupKeyForTOTP = 'GVGUT52HEZ3ZIRGBA2UTHSN44M'
        # totp = pyotp.TOTP(kiteSetupKeyForTOTP)
        # totp = totp.now()
        # obj=SmartConnect(api_key=apikey) # Praveen
        # # pdb.set_trace()
        # data = obj.generateSession(username,pwd,totp)
        # time.sleep(0.5)
        # # pdb.set_trace()
        # print("\n")
        # print("Praveen")
        # print(data)
        # refreshToken= data['data']['refreshToken']
        # #fetch the feedtoken
        # feedToken=obj.getfeedToken()
        # #fetch User Profile
        # userProfile= obj.getProfile(refreshToken)

        countt = 0
        countt = countt+1
        #apikey = 'DodjVpCE' # Sridharan knsridharan@winrich.in
        apikey = 'R5v5BgIG' 
        username = 'k31094'
        pwd = 'KnsAng@12#'
        pwd = '1985'
        kiteSetupKeyForTOTP = 'ZT4OKWGC3TXIRPRZJLDKX3IBCM'
        totp = pyotp.TOTP(kiteSetupKeyForTOTP)
        totp = totp.now()
        obj=SmartConnect(api_key=apikey) # Sridharan
        # pdb.set_trace()
        data = obj.generateSession(username,pwd,totp)
        time.sleep(0.5)
        # pdb.set_trace()
        print("\n")
        print("Sridharan")
        print(data)
        refreshToken= data['data']['refreshToken']
        #fetch the feedtoken
        feedToken=obj.getfeedToken()
        #fetch User Profile
        userProfile= obj.getProfile(refreshToken)

    except Exception as e:
        print("Error in login", e)

angelbrok_login()

def rms_check():
    global rmslimit
    while True:
        try:
            rmslimit = float(obj.rmsLimit()['data']['availablecash'])
            print("Cash Margin in account----> ", rmslimit)
            return rmslimit
            break
        except Exception as e:
            print("Login session Failed")
            print("we will relogin to angelbroking session again")
            print("\n")
            angelbrok_login()
            time.sleep(3)
rms_check()

obj_list =[obj]
obj_dict ={obj:"Sridharan"}
print("check obj")

def order_status():
    try:
        Trade_net = obj.position()['data'] # Angel Trade Net Positions
        nobj = obj_dict[obj]
        Trade_df=pd.DataFrame(Trade_net)
        #Angel_net_df = Trade_df[Trade_df['symbolname']== stock_id ]
        Trade_df.to_csv("Angel_net_positions_" + obj_dict[obj]+".csv")
        #print("Order status for stock ID:", stock_id)
        print(Trade_df)

    except Exception as e:
        print(obj_dict[obj], " ---> Order net positions subset csv file creation failed for :  ", nobj)
        print("\n")

order_status()

def angel_place_order(transaction_type, tsymbol, ttoken,tquantity): # Change Product type to MIS ----> INTRADAY (from ---> DELIVERY )
    global orderparams, orderId
    
    orderparams = {"variety": "NORMAL", "tradingsymbol": tsymbol, "symboltoken": ttoken, "transactiontype": transaction_type, "exchange": "NSE", "ordertype": "MARKET", "producttype": "DELIVERY", "duration": "DAY", "price": "0", "squareoff": "0", "stoploss": "0", "quantity": tquantity }
 
        
    print(orderparams)
    # pdb.set_trace()
    for name in obj_list:
        try:                    
                                                
            orderId=name.placeOrder(orderparams)
            print(obj_dict[name])
            print(tsymbol, " The order id is: {}".format(orderId))
            time_now = datetime.datetime.now().time().replace(microsecond=0)
            trade_dict_11 = {"time": time_now}
            print(trade_dict_11)
            print(time_now)
            print("\n")
                        

        except Exception as e:          
            print("\n")
            print(obj_dict[name], " ---> Order placement subset failed: for ", tsymbol)
            time_now = datetime.datetime.now().time().replace(microsecond=0)
            order_fail={"time":time_now, "name":obj_dict[name], "symbol":tsymbol}
            print(time_now)
            print("\n")

pdb.set_trace()

print('Buying CALL ----> ')
rms_check()

#if rmslimit > int(client_data['Praveen']):
    # Loop through each row in the dataframe
#dataframes = [df_Sridharan, df_Praveen, df_Ashok]  # List of your dataframes
#dataframes=[df_Praveen]
if os.path.isfile("List_Sridharan.csv"):
    df_Sridharan = pd.read_csv('List_Sridharan.csv',index_col=0)
    dataframes=[df_Sridharan]
    #df_Sridharan['Order_Placed']=False
    #df_Sridharan['Sell_Order_Placed'] = False
    #pdb.set_trace()
    if df_Sridharan.iloc[0]['Number_of_Stocks_Balance'] == 0:
        orders_placed = 0  # Counter variable to track the number of orders placed
    else:
        orders_placed = df_Sridharan.iloc[0]['Number_of_Stocks_Balance']
else:
    orders_placed=0
    #df_Sridharan['Order_Placed'] = False
placed_orders = set()  # Set to keep track of placed orders
#df['Order Placed'] = False  # Initialize the "Order Placed" column as False for all rows
while True: 
    for df in dataframes:
        #df['Order_Placed'] = False  # Initialize the "Order Placed" column as False for all rows
        for index, row in df.iterrows():
            stock_id = row['stock_id']
            trade_token = row['trade_token']
            number_of_stocks = row['number_of_stocks']
            last_high = row['Last High']
            ltp = obj.ltpData("NSE", stock_id, trade_token)['data']['ltp']
            time.sleep(1)
            print(ltp)

            # Check if the desired number of orders have been placed
            if orders_placed == 4:
                break

            #pdb.set_trace()
            #P_Orders=df.iloc[index]['Order_Placed']

            # Check if the stock ID is not already in orders_placed set
            if ltp > last_high and stock_id not in placed_orders and not row['Order_Placed']:
                print(f"Stock ID: {stock_id} - LTP: {ltp} - Placing BUY order for {number_of_stocks}")
                angel_place_order("BUY", stock_id, trade_token, number_of_stocks)
                time.sleep(1)
                order_status()

                df.at[index,'buy_price'] = ltp

                # Add the buying time to the dataframe
                df.at[index, 'buying_time'] = datetime.datetime.now()

                df.at[index, 'Order_Placed'] = True  # Set the "Order Placed" column as True for the current row
                orders_placed += 1  # Increment the counter for orders placed
                df['Number_of_Stocks_Balance']=orders_placed
                #pdb.set_trace()
                placed_orders.add(stock_id)  # Add stock_id to placed_orders set
            

        #df.drop(df.index[-1], inplace=True)
        df_Sridharan.to_csv('List_Sridharan.csv')
        print(df)

    if orders_placed >= 4:
        break
    time_now = dt.datetime.now().time().replace(microsecond=0)
    print(time_now)
    time.sleep(60)
    if time_now>=datetime.time(15,30,00):
        print("The Time is 15:30")
        sys.exit()
    time.sleep(5)


#df_Sridharan.to_csv('List_Sridharan.csv')
#df_Praveen.to_csv('List_Praveen.csv')
#df_Ashok.to_csv('List_Ashok.csv')
#pdb.set_trace()

print("\n")

#t = input("Do you want to execute the orders in your zerodha account (y/n): ")



