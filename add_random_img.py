import glob
if glob.glob("config.py"):
    import config
else:
    import github_config as config
import requests
from bs4 import BeautifulSoup as bs

user_agent = {'User-Agent': 'Mozilla/5.0'}


def main_img():
    session = requests.Session()
    novel = session.get(config.imgurl, headers=user_agent)
    novel.raise_for_status()
    print(novel.status_code)
    novel.encoding = "GBK"
    novelSoup = bs(novel.text, "html.parser")
    novel_img = novelSoup.find("img", {"id": "mainph"})
    novel_img = novel_img['src']
    img_data = requests.get(novel_img).content
    attachment_id = uploadImage(novel_img, img_data)
    return attachment_id

