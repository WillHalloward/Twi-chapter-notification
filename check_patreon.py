import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import secrets


async def patreon_check(page_created, chapter_title):
    page = requests.get("https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211",
                        cookies=secrets.cookies)
    json_data = json.loads(page.text)
    title = json_data['data'][0]['attributes']['title']
    title_san = re.sub(r'[^A-Za-z]', '', title)
    chapter_san = re.sub(r'[^A-Za-z]', '', chapter_title)
    patreon_time_converted = datetime.fromisoformat(json_data['data'][0]['attributes']['edited_at'])
    if page_created < patreon_time_converted and chapter_san in title_san:
        content = json_data['data'][0]['attributes']['content']
        soup = BeautifulSoup(content, "lxml")
        text = ""
        for br in soup.find_all("br"):
            br.replace_with("\n")
            text = "```" + soup.text.replace("\n", "```\n", 1)
        webhook = DiscordWebhook(url=secrets.patreon_spoilers)
        embed = DiscordEmbed(title='Password posted', description=title, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Post', value=text)
        webhook.add_embed(embed)
        webhook.content = "@here"
        webhook.execute()
        return False
    return True
