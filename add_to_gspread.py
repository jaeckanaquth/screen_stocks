import json
import screener
import glob
import gspread
import gspread_dataframe as gd
import pandas as pd
from bs4 import BeautifulSoup as bs
if glob.glob("config.py"):
    import config
else:
    import github_config as config

user_agent = {'User-Agent': 'Mozilla/5.0'}
name = "Stock of the Day"
count = 0

if not glob.glob("service_account.json"):
    service_account = json.loads(config.service_account)
    with open('service_account.json', 'w') as f:
        json.dump(service_account, f)
gc = gspread.service_account(filename="service_account.json")

try:
    sh = gc.open("QuthsStocks")
except:
    sh = gc.create("QuthsStocks")

try:
    worksheet = gc.open('QuthsStocks').worksheet(name)
except Exception as e:
    worksheet = sh.add_worksheet(title=name, rows="100", cols="2")

stock_df = pd.DataFrame(columns=["Name", "Company"])
df = pd.read_csv(
    'https://www1.nseindia.com/content/indices/ind_nifty50list.csv')
index_name = '^NSEI'  # S&P 500
published = screener.scr(stock_df, df, index_name)
if stock_df.shape[1] == 0:
    count = 1
    df = pd.read_csv('https://www1.nseindia.com/content/indices/ind_nifty500list.csv')
    index_name = '^CRSLDX'  # S&P 500
    published = screener.scr(stock_df, df, index_name)
if stock_df.shape[1] == 0:
    published = pd.read_csv(
        'https://www1.nseindia.com/content/indices/ind_nifty50list.csv')
gd.set_with_dataframe(worksheet, published)
print(published)
