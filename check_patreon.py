import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import logging
import secrets

headers = {
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}


async def patreon_check(page_created, chapter_title):
    logging.info("Requesting patreon api")
    page = requests.get("https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211",
                        cookies=secrets.cookies, headers=headers)
    json_data = json.loads(page.text)
    logging.info(f"Response {json_data}")
    title = json_data['data'][0]['attributes']['title']
    title_san = re.sub(r'[^A-Za-z]', '', title)
    chapter_san = re.sub(r'[^A-Za-z]', '', chapter_title)
    logging.info(f"Title {title}, title_san {title_san}, chapter_san {chapter_san}")
    patreon_time_converted = datetime.fromisoformat(json_data['data'][0]['attributes']['edited_at'])
    logging.info(f"Patreon_time_converted {patreon_time_converted}")
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
