import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import secrets


def patreon_check(page_created, chapter_title):
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=secrets.cookies)
    json_data = json.loads(page.text)
    title = json_data['data'][0]['attributes']['title']
    patreon_time = json_data['data'][0]['attributes']['edited_at']
    patreon_time_converted = datetime.strptime(patreon_time, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    patreon_time_converted = patreon_time_converted + timedelta(hours=2)
    if page_created < patreon_time_converted and title == chapter_title:
        content = json_data['data'][0]['attributes']['content']
        print(datetime.today().strftime('[%X:%f]') + " Found password")
        soup = BeautifulSoup(content, "lxml")
        text = ""
        for br in soup.find_all("br"):
            br.replace_with("\n")
            text = "```" + soup.text.replace("\n", "```\n", 1)
        print(datetime.today().strftime('[%X:%f]') + " Attempting to post to Discord")
        webhook = DiscordWebhook(url=secrets.patreon_spoilers)
        embed = DiscordEmbed(title='Password posted', description=title, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Post', value=text)
        webhook.add_embed(embed)
        webhook.content = "@here"
        webhook.execute()
        print(datetime.today().strftime('[%X:%f]') + " Succeeded to post to Discord")
        return False
    return True
