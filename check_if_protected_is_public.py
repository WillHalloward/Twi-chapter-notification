import time
from discord_webhook import DiscordWebhook
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import cookie

x = True
# url = "https://wanderinginn.com/2019/05/07/6-14-k/"
url = open("chapter.txt", "r").read()
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("header", {"class": "entry-header"})
    post_text = post.text.partition(' ')[0]
    if post_text == "\nProtected:":
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Chapter is Protected")
        time.sleep(10)
    else:
        print("Chapter is public")
        print(url)
        webhook = DiscordWebhook(url=cookie.spidey_webhook, content=url + " Chapter public")
        webhook.execute()
        x = False
