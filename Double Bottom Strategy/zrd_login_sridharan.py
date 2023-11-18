# https://www.youtube.com/watch?v=n04dtnMl_BU&list=PLifIWB1V-ILMpnExpxly40KhZ_gVVwHVm&index=12
# https://www.youtube.com/watch?v=B1jjo0zcE6g&list=PLifIWB1V-ILMpnExpxly40KhZ_gVVwHVm&index=13
# https://www.youtube.com/watch?v=wHLrMyzdgJw
import pdb
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
#import logging
#logging.basicConfig(level=logging.DEBUG)



#api_k = "a43v7sh3hkekai7u"
#api_s = "ni5pwigvj0k0vxxzzf9nc7qo1qlk4u1g"
#access_token="00obwJHA0kEMq4Xj9Qqyr000Hc4zJrjK"

api_k = "m8lqe0lp92mndpzw"
api_s = "lhg6sx4g3etshuleybete974h3voo8gz"
 

#access_token="PvshDH9vGWjg4VjUYBpY0LV1bbjJyrHY"
#access_token = "Qtn5gOWE77lvPH578VSaRV5SvH9LWDlY"
#Qtn5gOWE77lvPH578VSaRV5SvH9LWDlY

access_token = open('access_token1.txt').read()

# pdb.set_trace()


def get_login(api_k, api_s):
	print("logging into zerodha")
	global kws, kite
	kite = KiteConnect(api_key=api_k)

	# print("[*] Generate Request Token : ", kite.login_url())
	# request_tkn = input("[*] Enter Your Request Token Here : ")
	# data = kite.generate_session(request_tkn, api_secret=api_s)
	# kite.set_access_token(data["access_token"])
	# kws = KiteTicker(api_k, data["access_token"])
	# print(data['access_token'])

	kite.set_access_token(access_token)
	kws = KiteTicker(api_k, access_token)

	return kite

kite = get_login(api_k, api_s)
margins = kite.margins()

print(margins)


v=kite.quote('NSE:INDIA VIX')
bk=kite.quote('NSE:NIFTY BANK')
nk=kite.quote('NSE:NIFTY 50')

#bf=kite.quote('NFO:BANKNIFTY20DECFUT')
#nf=kite.quote('NFO:NIFTY20DECFUT')


print("\n")
print("(1.0) ", "VIX LTP -->", v['NSE:INDIA VIX']['last_price'], " & ", "VIX open for today -->", v['NSE:INDIA VIX']['ohlc']['open'], " & ", "VIX net change from yesterday -->", v['NSE:INDIA VIX']['net_change'])
print("\n")
print("(2.0) ", "BANK Nifty Index LTP  -->", bk['NSE:NIFTY BANK']['last_price'], " & ", "BANK Nifty Index open for today -->", bk['NSE:NIFTY BANK']['ohlc']['open'], " & ", "Bank Nifty Index net change from yesterday -->", bk['NSE:NIFTY BANK']['net_change'])
#print("(2.1) ", "BANKNifty FUTURES LTP -->", bf['NFO:BANKNIFTY20DECFUT']['last_price'])
print("\n")
print("(3.0) ", "NIFTY 50 Index LTP -->", nk['NSE:NIFTY 50']['last_price'], " & ", "NIFTY 50 Index open for today -->", nk['NSE:NIFTY 50']['ohlc']['open'], " & ", "NIFTY 50 Index net change from yesterday -->", nk['NSE:NIFTY 50']['net_change'])
#print("(3.1) ", "Nifty FUTURES LTP  -->", nf['NFO:NIFTY20DECFUT']['last_price'])
print("\n")



#pdb.set_trace()
#try:
#        order_id = kite.place_order(tradingsymbol="INFY",exchange=kite.EXCHANGE_NSE,variety=kite.VARIETY_REGULAR,
#                                transaction_type=kite.TRANSACTION_TYPE_BUY,
#                                quantity=1,
#                                order_type=kite.ORDER_TYPE_MARKET,
#                                product=kite.PRODUCT_NRML)
#
#        logging.info("Order placed. ID is: {}".format(order_id))
#except Exception as e:
#        logging.info("Order placement failed: {}".format(e.message))

nifty_50 = ["CIPLA","DRREDDY","SUNPHARMA","BPCL","ZEEL","IOC","TCS","ASIANPAINT","HINDALCO","INDUSINDBK","ONGC","MARUTI","TATASTEEL","BHARTIARTL","INFRATEL","NESTLEIND","HDFCBANK","TECHM","COALINDIA","ADANIPORTS","WIPRO","TATAMOTORS","EICHERMOT","RELIANCE","HEROMOTOCO","KOTAKBANK","BRITANNIA","BAJFINANCE","BAJAJFINSV","LT","ITC","M&M","HDFC","POWERGRID","NTPC","GRASIM","ULTRACEMCO","AXISBANK","HDFCLIFE","SBIN","GAIL","ICICIBANK","TITAN","SHREECEM","BAJAJ-AUTO","UPL","INFY","HCLTECH","HINDUNILVR","JSWSTEEL", "YESBANK"]
nifty_fno = ["CIPLA","LUPIN","DRREDDY","ADANIENT","FEDERALBNK","ASHOKLEY","SUNPHARMA","BPCL","VEDL","HINDPETRO","ZEEL","BHEL","IOC","TCS","PIDILITIND","ASIANPAINT","UBL","HINDALCO","PVR","TVSMOTOR","INDUSINDBK","ONGC","MARUTI","TATASTEEL","BHARTIARTL","SUNTV","MOTHERSUMI","INFRATEL","M&MFIN","NESTLEIND","PFC","MANAPPURAM","HDFCBANK","TECHM","COALINDIA","ADANIPORTS","AMARAJABAT","WIPRO","DLF","SRF","TATAMOTORS","RBLBANK","COLPAL","EICHERMOT","RELIANCE","BOSCHLTD","AMBUJACEM","SAIL","BALKRISIND","HEROMOTOCO","VOLTAS","KOTAKBANK","IBULHSGFIN","AUROPHARMA","BATAINDIA","DIVISLAB","CHOLAFIN","BRITANNIA","NMDC","BAJFINANCE","MARICO","BAJAJFINSV","BANKBARODA","LT","MUTHOOTFIN","ITC","TATAPOWER","RAMCOCEM","M&M","TATACONSUM","MINDTREE","BHARATFORG","HDFC","TATACHEM","TORNTPHARM","GLENMARK","POWERGRID","MGL","L&TFH","RECLTD","IGL","NTPC","GRASIM","BEL","CANBK","ESCORTS","EXIDEIND","ULTRACEMCO","LICHSGFIN","AXISBANK","HDFCLIFE","MCDOWELL-N","CADILAHC","IDFCFIRSTB","PNB","INDIGO","SBIN","GAIL","ICICIBANK","DABUR","HAVELLS","SRTRANSFIN","MFSL","BANDHANBNK","APOLLOTYRE","TITAN","PEL","SIEMENS","ICICIPRULI","SHREECEM","BAJAJ-AUTO","BIOCON","MRF","TORNTPOWER","ACC","SBILIFE","GODREJCP","UPL","PETRONET","PAGEIND","CONCOR","NAUKRI","APOLLOHOSP","GODREJPROP","HCLTECH","INFY","JUBLFOOD","NATIONALUM","JINDALSTEL","HINDUNILVR","COFORGE","GMRINFRA","IDEA","JSWSTEEL","CUMMINSIND","BERGEPAINT"]
watchlist = ["SBIN"]
#pdb.set_trace()
#kite.place_order(tradingsymbol='INFY', variety=kite.VARIETY_REGULAR, exchange=kite.EXCHANGE_NSE, transaction_type=kite.TRANSACTION_TYPE_BUY, quantity=1, order_type=kite.ORDER_TYPE_MARKET, product=kite.PRODUCT_MIS)
