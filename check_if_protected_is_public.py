import time
from datetime import datetime
import os

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import post_to_reddit
import secrets

print("[" + datetime.today().strftime('%X:%f') + "] Program start")
x = True
dir_path = os.path.dirname(os.path.realpath(__file__))
url = open(dir_path + "/chapter.txt", "r").read()
print("[" + datetime.today().strftime('%X:%f') + "] Attempting to reach " + url)
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("h1", {"class": "entry-title"})
    post_text = post.text.partition(' ')[0]
    if post_text == "Protected:":
        time.sleep(10)
    else:
        print("[" + datetime.today().strftime('%X:%f') + "] Chapter is Public")
        print(url)
        print(post.text)
        print("[" + datetime.today().strftime('%X:%f') + "] Attempting to post to Discord")
        webhook = DiscordWebhook(url=secrets.public_spoilers)
        embed = DiscordEmbed(title='Chapter public', description=post.text, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Link', value=url)
        webhook.add_embed(embed)
        webhook.execute()
        print("[" + datetime.today().strftime('%X:%f') + "] Succeeded to post to Discord")
        print("[" + datetime.today().strftime('%X:%f') + "] Attempting to post to reddit")
        post_to_reddit.post_to_reddit(post.text)
        print("[" + datetime.today().strftime('%X:%f') + "] Succeeded to post to reddit")
        x = False
print("[" + datetime.today().strftime('%X:%f') + "] Program finished")
