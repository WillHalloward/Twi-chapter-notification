import asyncio
from datetime import datetime

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import check_patreon
import secrets


async def main():
    conn = await asyncpg.connect('postgresql://postgres@localhost/testDB', user=secrets.DBuser, password=secrets.DBpass)
    today_date = datetime.today().strftime('%Y/%m/%d')
    x = True
    url = "https://wanderinginn.com/" + today_date
    while x:
        start_page = requests.get(url)
        if start_page.ok:
            soup = BeautifulSoup(start_page.content, "lxml", from_encoding="UTF-8")
            post = soup.find("h1", {"class": "entry-title"})
            p_date = soup.find("time", {"class": "entry-date"})
            p_date_converted = datetime.fromisoformat(p_date['datetime'])
            chapter = post.text.split(':')[1].strip()
            x = False
            y = True
            link_url = post.find('a')['href']
            conn.execute("INSERT INTO protected_is_public(url, title) VALUES ($1,$2)", link_url, chapter)
            webhook = DiscordWebhook(url=secrets.patreon_spoilers)
            embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
            embed.add_embed_field(name='Link', value=link_url)
            webhook.add_embed(embed)
            webhook.execute()
            while y:
                y = await check_patreon.patreon_check(p_date_converted, chapter)
        else:
            await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
