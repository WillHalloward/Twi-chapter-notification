import json
import clipboard
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from discord_webhook import DiscordWebhook

import cookie

def patreon_check(chapter):
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=cookie.cookies)
    json_data = json.loads(page.text)
    try:
        body = json_data['data'][0]['attributes']['content']
    except:
        print("No access")
        exit()
    title = json_data['data'][0]['attributes']['title']
    if title == chapter:
        soup = BeautifulSoup(body, "lxml")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        text = "```" + soup.text.replace("\n", "```\n", 1)
        link_url = soup.find("a").text
        textfile = open("chapter.txt", "w")
        print(title + "\n" + soup.text)
        clipboard.copy(title + "\n" + text)
        webhook = DiscordWebhook(url=cookie.spidey_webhook, content=title + "\n" + text)
        webhook.execute()
        textfile.write(link_url)
        return False
    else:
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Password not posted")
    return True
