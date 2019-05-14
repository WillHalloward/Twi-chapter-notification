import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import cookie

x = True
# url = "https://wanderinginn.com/2019/04/27/6-11/" #Testing
url = open("chapter.txt", "r").read()
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("h1", {"class": "entry-title"})
    print(post.text)
    post_text = post.text.partition(' ')[0]
    if post_text == "Protected:":
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Chapter is Protected")
        time.sleep(10)
    else:
        print("Chapter is public")
        print(url)
        print(post_text)
        webhook = DiscordWebhook(url=cookie.spidey_webhook)
        embed = DiscordEmbed(title='Chapter public', description=post.text, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Link', value=url)
        webhook.add_embed(embed)
        webhook.execute()
        x = False
