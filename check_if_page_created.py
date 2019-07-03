import os
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import check_patreon
import secrets

print(datetime.today().strftime('[%X:%f]') + " Program start")
today_date = datetime.today().strftime('%Y/%m/%d')
x = True
url = "https://wanderinginn.com/" + today_date
# url = "https://wanderinginn.com/2019/07/02/"
print(datetime.today().strftime('[%X:%f]') + " Attempting to reach " + url)
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml", from_encoding="UTF-8")
    check_404 = soup.find("article", {"id": "post-0"})
    if check_404 is None:
        print(datetime.today().strftime('[%X:%f]') + " Chapter is posted")
        post = soup.find("h1", {"class": "entry-title"})
        p_date = soup.find("time", {"class": "entry-date"})
        p_date_converted = datetime.strptime(p_date['datetime'], '%Y-%m-%dT%H:%M:%S+00:00')
        chapter = post.text.split(':')[1].strip()
        print(chapter)
        x = False
        y = True
        link_url = post.find('a')['href']
        print(link_url)
        print(datetime.today().strftime('[%X:%f]') + " Attempting to write to file")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        textfile = open(dir_path + "/chapter.txt", "w+")
        textfile.write(link_url)
        textfile.close()
        print(datetime.today().strftime('[%X:%f]') + " Succeeded to write to file")
        print(datetime.today().strftime('[%X:%f]') + " Attempting to post to Discord")
        webhook = DiscordWebhook(url=secrets.patreon_spoilers)
        embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Link', value=link_url)
        webhook.add_embed(embed)
        webhook.execute()
        print(datetime.today().strftime('[%X:%f]') + " Succeeded to post to Discord")
        print(datetime.today().strftime('[%X:%f]') + " Attempting to get password")
        while y:
            y = check_patreon.patreon_check(p_date_converted, chapter)
        print(datetime.today().strftime('[%X:%f]') + " Succeeded to get password")
    else:
        time.sleep(10)
print(datetime.today().strftime('[%X:%f]') + " Program finished")
