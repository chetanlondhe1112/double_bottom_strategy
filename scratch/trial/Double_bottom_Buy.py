"""double_bottom_buy"""
#import zrd_login as zl
import datetime as dt
import time
#import yfinance as yf
#import json
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
from sqlalchemy import create_engine,text
from functions.db_conn import sqlalchemy_connect
import requests
from datetime import date

sql=sqlalchemy_connect(username="chetan")

tables_dict=sql.read_config()
db_tables=tables_dict["db_tables"]
customer_tbl=db_tables["customer_table"]
user_table=db_tables["user_table"]
dbs_tickers_data_tbl=db_tables["dbs_tickers_data_table"]
dbs_customerpositions_data_tbl=db_tables["dbs_customerpositions_data_table"]
dbs_order_log_tbl=db_tables["dbs_order_log_table"]
# defaults
bnf_user="Sridharan"		#change username for bnf value generation from customer table
countt = 0
apikey = 'DodjVpCE' # Sridharan knsridharan@winrich.in

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

def angelbrok_loginv2(angel_obj,angel_user,angel_pwd,totp_key):   
	try:
                
		global feed_token, client_code, obj, obj3, obj4, obj5, obj6, obj7, obj8, obj9, obj10, obj11, obj12, obj13, obj14, obj16, obj17, obj20, obj21, obj22, obj23, password, refreshToken, accessToken, data
		
		countt = 0
		countt = countt+1
		username = angel_user
		#pwd = 'KnsAng@12#'
		pwd = angel_pwd
		kiteSetupKeyForTOTP = totp_key
		totp = pyotp.TOTP(kiteSetupKeyForTOTP)
		totp = totp.now()
		obj=angel_obj
		data = obj.generateSession(username,pwd,totp)
		refreshToken= data['data']['refreshToken']
		#fetch the feedtoken
		feedToken=obj.getfeedToken()
		#fetch User Profile
		userProfile= obj.getProfile(refreshToken)
    	
		return totp, obj 
       	
	except Exception as e:
        
	    print("Error in login", e)


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

def angel_place_order(transaction_type, tsymbol, ttoken,tquantity): # Change Product type to MIS ----> INTRADAY (from ---> DELIVERY )
    global orderparams, orderId
    
    orderparams = {"variety": "NORMAL", "tradingsymbol": tsymbol, "symboltoken": ttoken, "transactiontype": transaction_type, "exchange": "NSE", "ordertype": "MARKET", "producttype": "DELIVERY", "duration": "DAY", "price": "0", "squareoff": "0", "stoploss": "0", "quantity": tquantity }
 
        
    print(orderparams)
    # pdb.set_trace()
    for name in obj_list:
        try:                    
                                                
            #orderId=name.placeOrder(orderparams)
            orderId=333
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

def angel_place_orderv2(obj,transaction_type, tsymbol, ttoken,tquantity): # Change Product type to MIS ----> INTRADAY (from ---> DELIVERY )
    global orderparams, orderId
    
    orderparams = {"variety": "NORMAL", "tradingsymbol": tsymbol, "symboltoken": ttoken, "transactiontype": transaction_type, "exchange": "NSE", "ordertype": "MARKET", "producttype": "DELIVERY", "duration": "DAY", "price": "0", "squareoff": "0", "stoploss": "0", "quantity": tquantity }
 
        
    print(orderparams)
    # pdb.set_trace()
    #for name in obj_list:
    try:                    
                                            
        #orderId=name.placeOrder(orderparams)
        orderId=333
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

"""Customer data collection and object collection methods"""
def angelbrok_obj(apiky=str):
	return SmartConnect(api_key=apikey) # Sridharanss

def customer_data():
	all_cust={}
	customer_table_df=sql.fetch_tables(table_name=customer_tbl)[["name","angel_user","angel_pwd","totpkey","fin_q","apikey","asmita_apikey","status","strategyflag"]]
	customer_table_df=customer_table_df[(customer_table_df["status"]==1) & ((customer_table_df["strategyflag"]==2) | (customer_table_df["strategyflag"]==12))]
	for i in range(len(customer_table_df)):
		cus_df=customer_table_df.iloc[i].to_dict()
		all_cust[cus_df['name']]=cus_df
	print("\n All customers data\n",all_cust)
	return all_cust

def get_obj(customer_dict=dict):
	for i in customer_dict:
		cus_apikey=customer_dict[i]['asmita_apikey']
		username = customer_dict[i]['angel_user']
		pwd = int(sql.decrypt_password(customer_dict[i]["angel_pwd"]))
		print(pwd)
		totp_key=customer_dict[i]["totpkey"]

		print(username,pwd,totp_key)
		try:
			obj=angelbrok_obj(apiky=cus_apikey)
			totp,obj=angelbrok_loginv2(angel_obj=obj,angel_user=username,angel_pwd=pwd,totp_key=totp_key)
			print(totp,obj)
			customer_dict[i]["totp"]=int(totp)
			customer_dict[i]["obj"]=obj

		except Exception as e:
			customer_dict[i]["obj"]=0
			obj_val="Object Generation Failed '"+str(username)+"'"
			sql.error_log(error=e,validation=obj_val)
			print(e,obj_val)
			continue
	
	df=pd.DataFrame(customer_dict).T #convert the customer dict to dataframe and transpose
	df=df[df['obj']!=0].T	# Neglect the rows with 0 value in obj columns and aagain reverse transpose
	customer_dict=df.to_dict()
	print("\nCustomer dictionary with object and totp\n",customer_dict)
	return customer_dict

def get_key(val):
	for key,value in obj_dict.items():
		if str(val)==str(value):
			return key

def obj_ls_di(cus_obj_dict=dict):
	obj_list =[] 
	obj_dict ={}
	for i in all_cust:
		obj_list.append(all_cust[i]['obj'])
		obj_dict[all_cust[i]['name']]=all_cust[i]['obj']
	print("\nobjlist\n",obj_list)
	print("\nobj dict\n",obj_dict)
	return obj_list,obj_dict


all_cust=customer_data()

all_cust=get_obj(customer_dict=all_cust)	#updated dictionary with objects
print("new dict",all_cust)
#clean up customer dict if the angel objects are not formed for a particular customer
obj_list,obj_dict=obj_ls_di(cus_obj_dict=all_cust)
print(obj_list)

#order_status()
#angelbrok_login()
#rms_check()

print('Buying CALL ----> ')

#if rmslimit > int(client_data['Praveen']):
    # Loop through each row in the dataframe
#dataframes = [df_Sridharan, df_Praveen, df_Ashok]  # List of your dataframes
#dataframes=[df_Praveen]

if os.path.isfile("F:/project-12/double_bottom_strategy/scratch/trial/List_Sridharan.csv"):
    df_Sridharan = pd.read_csv('F:/project-12/double_bottom_strategy/scratch/trial/List_Sridharan.csv',index_col=0)
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
"""
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
"""

yesterday=datetime.datetime.now()-datetime.timedelta(1)
df=sql.fetch_tables(table_name=dbs_tickers_data_tbl)
print(df)

url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
d = requests.get(url).json()
token_df = pd.DataFrame.from_dict(d)
print(token_df)

def get_ltp_value(stock):
    ltp = obj.ltpData("NSE", stock, "26009")['data']['ltp']
    old_bnf_ltp=ltp
    print(ltp)
    return ltp


for stock in df['stock_id']:
    print(stock)
    token_value=token_df[token_df['symbol']==stock]['token']
    print(int(token_value))
    ltp=get_ltp_value(stock=stock)
    high_value=int(df[df['stock_id']==stock]['Last High'])
    print(high_value)
    for obj in obj_list:
        ang_user=get_key(obj)	
        print(obj,ang_user)
        fin_q=all_cust[ang_user]['fin_q']
        customer_positions_data=sql.fetch_tables(table_name=dbs_customerpositions_data_tbl)
        customer_positions_data=customer_positions_data[customer_positions_data['customer_name']==ang_user]
        customer_positions_data=customer_positions_data[customer_positions_data['stock_id']==stock]
        customer_positions=len(customer_positions_data)
        print(customer_positions)
        # Check if the desired number of orders have been placed
        if orders_placed == 4:
            break

        #pdb.set_trace()
        #P_Orders=df.iloc[index]['Order_Placed']

        # Check if the stock ID is not already in orders_placed set
        if ltp > high_value and stock not in customer_positions_data['stock_id']:#" and not row['Order_Placed']:
            print(f"Stock ID: {stock} - LTP: {ltp} ")#- Placing BUY order for {number_of_stocks}")
            angel_place_order("BUY", stock, token_value,tquantity=0)#, number_of_stocks)
        
        #   time.sleep(1)
        #   order_status()

        #   df.at[index,'buy_price'] = ltp

        #    # Add the buying time to the dataframe
        #    df.at[index, 'buying_time'] = datetime.datetime.now()

        #    df.at[index, 'Order_Placed'] = True  # Set the "Order Placed" column as True for the current row
        #    orders_placed += 1  # Increment the counter for orders placed
        #    df['Number_of_Stocks_Balance']=orders_placed
        #    #pdb.set_trace()
        #    placed_orders.add(stock_id)  # Add stock_id to placed_orders set
        #angel_place_order(obj,"SELL", PE_Symbol, PE_Token,fin_q=fin_q)
        #time.sleep(3)
        #order_status(obj=obj,sellflag="0")
#df_Sridharan.to_csv('List_Sridharan.csv')
#df_Praveen.to_csv('List_Praveen.csv')
#df_Ashok.to_csv('List_Ashok.csv')
#pdb.set_trace()

print("\n")

#t = input("Do you want to execute the orders in your zerodha account (y/n): ")



