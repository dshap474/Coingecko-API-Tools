"""
Function to receive the date, time, price, market cap, and volume for any 
Coingecko token.

Created on Thu Aug 31 10:18:31 2023
@author: dansh
"""

import requests
import pandas as pd
import datetime
from datetime import datetime
pd.set_option("display.max_columns", None)

def Coingecko_DF(coin_id, vs_currency='usd', days='max', interval='daily', start='none', end='none'):
    
    ###########################################################################
    #                        Create the DataFrame
    ###########################################################################
    # Pull data and create initial dataframe
    req = requests.get("https://api.coingecko.com/api/v3/coins/" + coin_id + "/market_chart?vs_currency=" + vs_currency + "&days=" + days + "&interval=" + interval)
    data = req.json()
    df = pd.DataFrame.from_dict(data)

    # Create the time column and add it to the dataframe
    time = []
    i = 0
    while i < len(df):
        time.append(df.iloc[i,0][0])
        i += 1
    df.insert(loc=0, column = 'time', value=time)
    
    # Price
    price = []
    i=0
    while i < len(df):
        price.append(df.iloc[i][1][1])
        i += 1
    df.insert(loc=4, column = 'price', value = price)
    
    # Market Cap
    mcap = []
    i=0
    while i < len(df):
        mcap.append(df.iloc[i][2][1])
        i += 1
    df.insert(loc=4, column = 'mcap', value = mcap)
    
    # Volume
    volume = []
    i=0
    while i < len(df):
        volume.append(df.iloc[i][3][1])
        i += 1
    df.insert(loc=4, column = 'volume', value = volume)
    
    # Add Date
    df['date'] = pd.to_datetime(df["time"], unit='ms')
    
    df = df.drop(columns=['prices', 'market_caps', 'total_volumes'])
    df = df[['date', 'time', 'price', 'volume', 'mcap']]
    
    ###########################################################################
    #        Check Conditionals and create outputs for the Function
    ###########################################################################
    # Full Date History
    if start == 'none' and end == 'none':
        return df
    
    # If there is a start and/or end date entered
    else:
        
        # Get current time
        now = datetime.now().timestamp()
            
        # Beginning of data to an end point
        if start == 'none' and end != 'none':
            
            # Get timestamps
            end_time = datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timestamp() 
            
            # Conditional Time Checks
            if end_time > now:
                print('This function can not see into the future!')
            elif df.time[0]/1000 < end_time:
                df = df[  df.index[0] : df[df['date']==end].index[0]  ]
                df = df.reset_index()
                df = df[['date', 'time', 'price', 'volume', 'mcap']]
                return df
            else:
                print('The entered END time is before the token existed')
            
        
        # Some start point to present time
        if start != 'none' and end == 'none':
            
            # Get timestamps
            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").timestamp()
            
            # Conditional Time Checks
            if start_time > now:
                print('This function can not see into the future!')   
            elif df.time[0]/1000 < start_time:
                df = df[  df[df['date']==start].index[0] : df.index[-1]  ]
                df = df.reset_index()
                df = df[['date', 'time', 'price', 'volume', 'mcap']]
                return df
            else:
                print('The entered START time is before the token existed')
            
            
        # If a beginning and end date are entered
        if start != 'none' and end != 'none':   
            
            # Get timestamps
            start_time = datetime.strptime(start, "%Y-%m-%d %H:%M:%S").timestamp()
            end_time   = datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timestamp() 
            
            # Conditional Time Checks
            if start_time > end_time:
                print('The START time can not be after the END time!')
            elif start_time > now or end_time > now:
                print('This function can not see into the future!')
            elif  df.time[0]/1000 < start_time and start_time < end_time:
                df = df[  df[df['date']==start].index[0]  :  df[df['date']==end].index[0]  ]
                df = df.reset_index()
                df = df[['date', 'time', 'price', 'volume', 'mcap']]
                return df
            else:
                return print('The entered start time is before the token existed')
    
    
        
        
        
    
    
    
    
    
    