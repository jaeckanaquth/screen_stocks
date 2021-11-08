import json, time
import screener
import add_random_img
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


if config.head == "Chosen from NIFTY 50":
    name = "NIFTY 50"
    df = pd.read_csv(
        'https://www1.nseindia.com/content/indices/ind_nifty50list.csv')
    index_name = '^NSEI'
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
        worksheet.clear()
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="7")
    published = screener.screening(df, index_name)
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
        worksheet = sh.add_worksheet(title=name, rows="100", cols="7")
    if config.count == 0:
        worksheet.clear()
        published = screener.screening(df, index_name)
        gd.set_with_dataframe(worksheet, published)
    else:
        published = pd.DataFrame(worksheet.get_all_records())
        _ = screener.screening(df, index_name)
        published = published.append(_)
        gd.set_with_dataframe(worksheet, published)

content = ''
if config.count == 4:
    name = "NIFTY 50"
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="7")
    published = pd.DataFrame(worksheet.get_all_records())
    content = '<h3>Chosen from NIFTY 50</h3> <br /> <p><figure>'
    content = content + published.to_html(index=False) + '</figure></p>'
    name = "NIFTY 500"
    try:
        worksheet = gc.open('QuthsStocks').worksheet(name)
    except Exception as e:
        worksheet = sh.add_worksheet(title=name, rows="100", cols="7")
    published = pd.DataFrame(worksheet.get_all_records())
    content = content + '<br /> <body> <h3>Chosen from NIFTY 500</h3> <br /> <p> <figure>'
    content = content + published.to_html(index=False) + "</figure> </p>"
    content = content + '''<br /><pre>Publisher: QuthCodes </pre> <br /> <footer><footer style="font-size: 60%; text-align: justify;">
<p>The information contained in this website is general information for study purposes only. We make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability or availability with respect to the website or the information, products, services, or related graphics contained on the website for any purpose. Any reliance you place on such information is therefore strictly at your own risk.<br />In no event will we be liable for any loss or damage including without limitation, indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits arising out of, or in connection with, the use of this website.<br />Through this website you are able to link to other websites which are not under the control of Quths.com. We have no control over the nature, content and availability of those sites. The inclusion of any links does not necessarily imply a recommendation or endorse the views expressed within them.<br />Every effort is made to keep the website up and running smoothly. However, Quths.com takes no responsibility for, and will not be liable for, the website being temporarily unavailable due to technical issues beyond our control.</p>
</footer></footer>'''
    
    attachment_id = add_random_img.main_img()

    try:
        posted = goes_to_wp.posting(content)
        attach_img = goes_to_wp.attachment_img(attachment_id)
    except:
        time.sleep(20)
        posted = goes_to_wp.posting(content)
        attach_img = goes_to_wp.attachment_img(attachment_id)
    print(published)
