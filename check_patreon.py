import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

import cookie

def patreon_check(chapter):
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=cookie.cookies)
    json_data = json.loads(page.text)
    try:
        body = json_data['data'][1]['attributes']['content']
    except:
        print("No access")
        exit()
    title = json_data['data'][1]['attributes']['title']
    if title == chapter:
        soup = BeautifulSoup(body, "lxml")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = "```" + soup.text.replace("\n", "```\n", 1)
        link_url = soup.find("a").text
        textfile = open("chapter.txt", "w")
        print(title + "\n" + soup.text)
        webhook = DiscordWebhook(url=cookie.spidey_webhook)
        embed = DiscordEmbed(title='Password posted', description=title, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Post', value=text)
        webhook.add_embed(embed)
        webhook.execute()
        textfile.write(link_url)
        return False
    else:
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Password not posted")
    return True
