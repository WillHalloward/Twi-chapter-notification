import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import cookie


def patreon_check(chapter):
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=cookie.cookies)
    json_data = json.loads(page.text)
    try:
        content = json_data['data'][0]['attributes']['content']
    except:
        print("No access")
        exit()
    title = json_data['data'][0]['attributes']['title']
    post_type = json_data['data'][0]['attributes']['post_type']
    if title == chapter and post_type == "text_only":
        soup = BeautifulSoup(content, "lxml")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = "```" + soup.text.replace("\n", "```\n", 1)
        link_url = soup.find("a").text
        textfile = open("chapter.txt", "w")
        print(title + "\n" + soup.text)
        webhook = DiscordWebhook(url=cookie.patreon_spoilers)
        embed = DiscordEmbed(title='Password posted', description=title, color=000000)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
        embed.add_embed_field(name='Post', value=text)
        webhook.add_embed(embed)
        webhook.execute()
        textfile.write(link_url)
        return False
    else:
        print("[" + datetime.today().strftime('%X') + "] Password not posted")
    return True
