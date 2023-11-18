import pandas as pd
from SmartApi.smartConnect import SmartConnect
import datetime
import time
import mibian
import pyotp
import sys
import pdb
import datetime as dt

def angelbrok_login():
    try:
        global feed_token, client_code, obj, password, refreshToken, accessToken, data
        
        # countt = 0
        # countt = countt+1
        # apikey = 'rHUQcZsN' 
        # username = 'P52012673'
        # pwd = 'Pk@123'
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
    global orderparams
    
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

#pdb.set_trace()

# Read the CSV file using pandas
#df_Sridharan = pd.read_csv('List_Sridharan.csv',index_col=0)
df_Sridharan = pd.read_csv('List_Sridharan.csv',index_col=0)
#df_Ashok = pd.read_csv('List_Ashok.csv',index_col=0)
#print(df_Sridharan)
print(df_Sridharan)
pdb.set_trace()
#print(df_Ashok)

# Loop through each row in the DataFrame
dataframes = [df_Sridharan]
sell_placed_orders = set()
orders_placed=df_Sridharan['Number_of_Stocks_Balance']
while True: 
    for df in dataframes:
        for index, row in df.iterrows():
            stock_id = row['stock_id']
            trade_token = row['trade_token']
            number_of_stocks = row['number_of_stocks']
            TakeProfit = row['TakeProfit']
            StopLoss = row['Stop Loss']
            #trigger_prices=row['trigger_prices']

            # Call the ltpData method to get the ltp for the current row
            ltp = obj.ltpData("NSE", stock_id, trade_token)['data']['ltp']

            # Check if ltp > take_profit
            #pdb.set_trace()
            if ltp > TakeProfit and row['SELL_Order_Placed']==False and row['Order_Placed']==True:
                print(f"Stock ID: {stock_id} - LTP: {ltp} - Placing SELL order for {number_of_stocks}")
                angel_place_order("SELL", stock_id, trade_token, number_of_stocks)
                time.sleep(1)
                #pdb.set_trace()
                order_status()

                df.at[index,'SELL_price'] = ltp

                # Add the buying time to the dataframe
                df.at[index, 'selling_time'] = datetime.datetime.now()

                df.at[index, 'SELL_Order_Placed'] = True  # Set the "Order Placed" column as True for the current row
                orders_placed -= 1  # Decrement the counter for orders placed
                df['Number_of_Stocks_Balance']=orders_placed
                #sell_placed_orders.add(stock_id)  # Add stock_id to placed_orders set

            # Check if ltp < stop_loss
            elif ltp < StopLoss and row['SELL_Order_Placed']==False and row['Order_Placed']==True:
                print(f"Stock ID: {stock_id} - LTP: {ltp} - Placing SELL order for {number_of_stocks}")
                angel_place_order("SELL", stock_id, trade_token, number_of_stocks)
                time.sleep(1)
                order_status()

                df.at[index,'SELL_price'] = ltp

                # Add the buying time to the dataframe
                df.at[index, 'selling_time'] = datetime.datetime.now()

                df.at[index, 'SELL_Order_Placed'] = True  # Set the "Order Placed" column as True for the current row
                orders_placed -= 1  # Decrement the counter for orders placed
                df['Number_of_Stocks_Balance']=orders_placed
                #sell_placed_orders.add(stock_id)  # Add stock_id to placed_orders set

            elif row['SELL_Order_Placed']==False :
                print(f"Stock ID: {stock_id} - LTP: {ltp} - No action taken")
                time.sleep(1)
                continue

        print(df)
        df_Sridharan.to_csv('List_Sridharan.csv')

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
