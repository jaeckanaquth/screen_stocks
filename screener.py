# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:48:18 2020

@author: jaeck
"""
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
import datetime, time


def scr(stock_df, df, index_name):
    n = -1
    
    # print(stock_df)

    yf.pdr_override()

    

    stocklist = df['Symbol'].to_list()
    name = df['Company Name'].to_list()

    exportList = pd.DataFrame(columns=['Stock', "RS_Rating", "50 Day MA",
                          "150 Day Ma", "200 Day MA", "52 Week Low", "52 week High"])

    for stock, na in zip(stocklist[1:], name[1:]):
        # print(n)
        try:
            stock = stock + '.NS'
            n += 1
            time.sleep(5)
            
            print ("pulling '{}' with index {}".format(na, n))
        
            # RS_Rating 
            start_date = datetime.datetime.now() - datetime.timedelta(days=365)
            end_date = datetime.date.today()
            
            df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
            df['Percent Change'] = df['Adj Close'].pct_change()    
            stock_return = df['Percent Change'].sum() * 100
            
            index_df = pdr.get_data_yahoo(index_name, start=start_date, end=end_date)
            index_df['Percent Change'] = index_df['Adj Close'].pct_change()
            index_return = index_df['Percent Change'].sum() * 100
            
            RS_Rating = round((stock_return / index_return) * 10, 2)
            # print(RS_Rating)
            # print(df.head(1))
            try:
                sma = [50, 150, 200]
                for x in sma:
                    df["SMA_"+str(x)] = round(df['Adj Close'].rolling(window=x).mean(), 2)

                # Storing required values
                currentClose = df["Adj Close"][-1]
                moving_average_50 = df["SMA_50"][-1]
                moving_average_150 = df["SMA_150"][-1]
                moving_average_200 = df["SMA_200"][-1]
                low_of_52week = round(min(df["Low"][-260:]), 2)
                high_of_52week = round(max(df["High"][-260:]), 2)

                try:
                    moving_average_200_20 = df["SMA_200"][-20]
                except Exception:
                    moving_average_200_20 = 0

                # Condition 1: Current Price > 150 SMA and > 200 SMA
                condition_1 = currentClose > moving_average_150 > moving_average_200

                # Condition 2: 150 SMA and > 200 SMA
                condition_2 = moving_average_150 > moving_average_200

                # Condition 3: 200 SMA trending up for at least 1 month
                condition_3 = moving_average_200 > moving_average_200_20

                # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
                condition_4 = moving_average_50 > moving_average_150 > moving_average_200

                # Condition 5: Current Price > 50 SMA
                condition_5 = currentClose > moving_average_50

                # Condition 6: Current Price is at least 30% above 52 week low
                condition_6 = currentClose >= (1.3*low_of_52week)

                # Condition 7: Current Price is within 25% of 52 week high
                condition_7 = currentClose >= (.75*high_of_52week)

                condition_8 = RS_Rating >= 7
        
                if(condition_1 and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7 and condition_8):
                    print("made it")
                    na = na.replace("'","")
                    dct = {"name":stock, "company": na }
                    stock_df = stock_df.append(dct, ignore_index=True)
                    print(stock_df)
            except Exception as e:
                print("Error Ouccured" + str(e))
                time.sleep(10)
                pass
        except Exception as e:
            print("Error Ouccured: " + str(e))
            time.sleep(10)
            pass
    try:
        print(stock_df)
        return stock_df
    except:
        print("Someting went wrong")
