import asyncio

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import post_to_reddit
import secrets


async def main():
    conn = await asyncpg.connect('postgresql://postgres@localhost/testDB', user=secrets.DBuser, password=secrets.DBpass)
    url = conn.fetchrow("SELECT url FROM protected_is_public ORDER BY serial_id DESC LIMIT 1")
    while True:
        startPage = requests.get(url['url'])
        if "post-password-form" in startPage.text:
            await asyncio.sleep(10)
        else:
            soup = BeautifulSoup(startPage.content, "lxml")
            post = soup.find("h1", {"class": "entry-title"})
            webhook = DiscordWebhook(url=secrets.public_spoilers)
            embed = DiscordEmbed(title='Chapter public', description=post.text, color=000000)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
            embed.add_embed_field(name='Link', value=startPage.url)
            webhook.add_embed(embed)
            webhook.execute()
            post_to_reddit.post_to_reddit(post.text, url)
            break


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
