from kiteconnect import KiteConnect
from kiteconnect import KiteTicker

import datetime

import time


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)

print(current_time)


s = time.time(); import pandas as pd; time.time() - s

print(time.time() - s)

import pdb

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)



kws = ""
kite = ""



api_k = "m8lqe0lp92mndpzw"
api_s = "lhg6sx4g3etshuleybete974h3voo8gz"
 



def get_login(api_k, api_s):  # log in to zerodha API panel
    global kws, kite
    kite = KiteConnect(api_key=api_k)
    print("[*] Generate access Token : ", kite.login_url())
    #https://kite.trade/connect/login?api_key=a43v7sh3hkekai7u for request token https://kite.trade/connect/login?api_key=a43v7sh3hkekai7u&v=3

    request_tkn = input("[*] Enter Your Request Token Here : ")
    data = kite.generate_session(request_tkn, api_secret=api_s)
    kite.set_access_token(data["access_token"])
    kws = KiteTicker(api_k, data["access_token"])
    print(data['access_token'])

    # kite.set_access_token(access_token)
    # kws = KiteTicker(api_k, access_token)


get_login(api_k, api_s)

pdb.set_trace()


