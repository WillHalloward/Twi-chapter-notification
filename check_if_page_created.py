import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import check_patreon
import secrets

today_date = datetime.today().strftime('%Y/%m/%d')
x = True
url = "https://wanderinginn.com/" + today_date
# url = "https://wanderinginn.com/2019/05/21/"

while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    check_404 = soup.find("article", {"id": "post-0"})
    if check_404 is None:
        post = soup.find("h1", {"class": "entry-title"})
        p_date = soup.find("time", {"class": "entry-date"})
        print(p_date)
        p_date_converted = datetime.strptime(p_date['datetime'], '%Y-%m-%dT%H:%M:%S+00:00')
        chapter = post.text.split(':')[1].strip()
        print(chapter)
        print("Chapter is posted")
        x = False
        y = True
        link_url = post.find('a')['href']
        print(link_url)
        textfile = open("chapter.txt", "w+")
        textfile.write(link_url)
        textfile.close()
        webhook = DiscordWebhook(url=secrets.patreon_spoilers)
        embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Link', value=link_url)
        webhook.add_embed(embed)
        webhook.execute()
        while y:
            y = check_patreon.patreon_check(p_date_converted, chapter)

    else:
        print("[" + datetime.today().strftime('%X') + "] Chapter is not created")
        time.sleep(10)
