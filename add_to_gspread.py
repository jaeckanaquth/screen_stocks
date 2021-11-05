import json
import screener
import glob
import gspread
import gspread_dataframe as gd
import pandas as pd
import goes_to_wp
from bs4 import BeautifulSoup as bs
if glob.glob("config.py"):
    import config
else:
    import github_config as config

user_agent = {'User-Agent': 'Mozilla/5.0'}

if not glob.glob("service_account.json"):
    service_account = json.loads(config.service_account)
    with open('service_account.json', 'w') as f:
        json.dump(service_account, f)
gc = gspread.service_account(filename="service_account.json")

try:
    sh = gc.open("QuthsStocks")
except:
    sh = gc.create("QuthsStocks")


stock_df = pd.DataFrame(columns=["name", "company"])

if config.head == "Chosen from NIFTY 50":
    name = "NIFTY 50"
    df = pd.read_csv(
        'https://www1.nseindia.com/content/indices/ind_nifty50list.csv')
    index_name = '^NSEI'
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="2")
    published = screener.scr(stock_df, df, index_name)
    gd.set_with_dataframe(worksheet, published)

if config.head == "Chosen from NIFTY 500":
    name = "NIFTY 500"
    df = pd.read_csv(
        'https://www1.nseindia.com/content/indices/ind_nifty500list.csv')
    count_to = config.count * 100 + 100
    df = df[config.count * 100:count_to]
    index_name = '^CRSLDX'
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="2")
    if config.count == 0:
        published = screener.scr(stock_df, df, index_name)
        gd.set_with_dataframe(worksheet, published)
    else:
        published = pd.DataFrame(worksheet.get_all_records())
        _ = screener.scr(stock_df, df, index_name)
        published = published.append(_)
        gd.set_with_dataframe(worksheet, published)

if config.count == 4:
    name = "NIFTY 50"
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="2")
    published = pd.DataFrame(worksheet.get_all_records())
    content = '<h2>Chosen from NIFTY 50</h2> <br /> <figure class="wp-block-table">'
    content = content + published.to_html() + '</figure>'
    name = "NIFTY 500"
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="2")
    published = pd.DataFrame(worksheet.get_all_records())
    content = content + '<br /> <body> <h2>Chosen from NIFTY 500</h2> <br /> <figure class="wp-block-table">'
    content = content + published.to_html() + "</figure>"
    

    goes_to_wp.posting(content)
    print(published)
