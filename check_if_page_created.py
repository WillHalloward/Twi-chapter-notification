import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import check_patreon
import cookie

today_date = datetime.today().strftime('%Y/%m/%d')
x = True
url = "https://wanderinginn.com/" + today_date
# url = "https://wanderinginn.com/2019/05/11/6-15-k/"
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("h1", {"class": "entry-title"})
    if post.text != "This is somewhat embarrassing, isn’t it?":
        post_text = post.text.split(' ')[0]
        chapter = post.text.split(':')[1]
        chapter = chapter.strip()
        print(chapter)
        if post_text == "Protected:":
            print("Chapter is posted")
            x = False
            y = True
            link_url = post.find('a')['href']
            webhook = DiscordWebhook(url=cookie.spidey_webhook)
            embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
            embed.add_embed_field(name='Link', value=link_url)
            webhook.add_embed(embed)
            webhook.execute()
            while y:
                time.sleep(1)
                y = check_patreon.patreon_check(chapter)

    else:
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Chapter is not created")
        time.sleep(10)
