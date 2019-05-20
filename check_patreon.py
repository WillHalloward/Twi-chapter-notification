import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import cookie


def patreon_check(page_created):
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=cookie.cookies)
    json_data = json.loads(page.text)
    content = json_data['data'][0]['attributes']['content']
    title = json_data['data'][0]['attributes']['title']
    patreon_time = json_data['data'][0]['attributes']['edited_at']
    patreon_time_converted = datetime.strptime(patreon_time, '%Y-%m-%dT%H:%M:%S.%f+00:00')
    patreon_time_converted = patreon_time_converted + timedelta(hours=2)
    if page_created < patreon_time_converted:
        soup = BeautifulSoup(content, "lxml")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = "```" + soup.text.replace("\n", "```\n", 1)
        print(title + "\n" + soup.text)
        webhook = DiscordWebhook(url=cookie.spidey_bot)
        embed = DiscordEmbed(title='Password posted', description=title, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Post', value=text)
        webhook.add_embed(embed)
        webhook.content = "@here"
        webhook.execute()
        return False
    else:
        print("[" + datetime.today().strftime('%X') + "] Password not posted")
    return True
