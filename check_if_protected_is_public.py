import asyncio
import logging
import os
import ssl
import sys

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import get_wordpress
import post_to_reddit
import secrets

home = os.path.expanduser('~')
logging.basicConfig(filename=f'{home}/Twi-chapter-notification/public.log',
                    format='%(asctime)s :: %(levelname)-8s :: %(filename)s :: %(message)s',
                    level=logging.INFO)
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_verify_locations(f"{home}/ssl-cert/server-ca.pem")
context.load_cert_chain(f"{home}/ssl-cert/client-cert.pem", f"{home}/ssl-cert/client-key.pem")
logging.basicConfig(filename=f'{home}/twi_bot_shard/cognita.log',
                    format='%(asctime)s :: %(levelname)-8s :: %(filename)s :: %(message)s',
                    level=logging.DEBUG)
logging.info("chapter protected check starting")


async def main():
    try:
        conn = await asyncpg.connect(database=secrets.database, user=secrets.DB_user,
                                     password=secrets.DB_password,
                                     host=secrets.host, ssl=context)
    except Exception as e:
        logging.critical(f"{type(e).__name__} - {e}")
        sys.exit("Failed to connect to database")
    url = await conn.fetchrow("SELECT url FROM protected_is_public ORDER BY serial_id DESC LIMIT 1")
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    logging.info("Starting request loop")
    while True:
        startPage = requests.get(url['url'], headers=headers)
        if "post-password-form" in startPage.text:
            await asyncio.sleep(10)
        else:
            logging.info("Found a match in page")
            soup = BeautifulSoup(startPage.content, "lxml")
            post = soup.find("h1", {"class": "entry-title"})
            logging.info(f"Found title {post.text}")
            webhook = DiscordWebhook(url=secrets.public_spoilers)
            embed = DiscordEmbed(title='Chapter public', description=post.text, color=000000)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
            embed.add_embed_field(name='Link', value=startPage.url)
            webhook.add_embed(embed)
            logging.info("Sending to discord")
            webhook.execute()
            logging.info("Posting to reddit")
            post_to_reddit.post_to_reddit(post.text, url['url'])
            break
    logging.info("Starting get_wordpress")
    await get_wordpress.get_wordpress(startPage, conn)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
