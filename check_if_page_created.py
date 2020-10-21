import asyncio
import logging
import os
import ssl
import sys
from datetime import datetime, timezone

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed

import check_patreon
import get_patreon
import secrets

home = os.path.expanduser('~')
logging.basicConfig(filename=f'{home}/Twi-chapter-notification/patreon.log',
                    format='%(asctime)s :: %(levelname)-8s :: %(filename)s :: %(message)s',
                    level=logging.INFO)
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.load_verify_locations(f"{home}/ssl-cert/server-ca.pem")
context.load_cert_chain(f"{home}/ssl-cert/client-cert.pem", f"{home}/ssl-cert/client-key.pem")
logging.basicConfig(filename=f'{home}/twi_bot_shard/cognita.log',
                    format='%(asctime)s :: %(levelname)-8s :: %(filename)s :: %(message)s',
                    level=logging.DEBUG)
logging.info("chapter created check starting")


async def main():
    try:
        conn = await asyncpg.connect(database=secrets.database, user=secrets.DB_user,
                                     password=secrets.DB_password,
                                     host=secrets.host, ssl=context)
    except Exception as e:
        logging.critical(f"{type(e).__name__} - {e}")
        sys.exit("Failed to connect to database")
    headers = {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }
    x = True
    while x:
        url = "https://wanderinginn.com/" + datetime.now(timezone.utc).strftime('%Y/%m/%d')
        logging.info(f"Requesting {url}")
        start_page = requests.get(url, headers=headers)
        logging.info(f"Requst answer {start_page}")
        if start_page.ok:
            soup = BeautifulSoup(start_page.content, "lxml", from_encoding="UTF-8")
            post = soup.find("h1", {"class": "entry-title"})
            p_date = soup.find("time", {"class": "entry-date"})
            p_date_converted = datetime.fromisoformat(p_date['datetime'])
            logging.info(f"Post date: {p_date_converted}")
            chapter = post.text.split(':')[1].strip()
            x = False
            y = True
            link_url = post.find('a')['href']
            logging.info(f"Inserting into database {link_url}, {chapter}")
            await conn.execute("INSERT INTO protected_is_public(url, title) VALUES ($1,$2)", link_url, chapter)
            webhook = DiscordWebhook(url=secrets.patreon_spoilers)
            embed = DiscordEmbed(title='New chapter', description=chapter, color=000000)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/attachments/577548376929992734/577866147236544513/erin.png')
            embed.add_embed_field(name='Link', value=link_url)
            webhook.add_embed(embed)
            resp = webhook.execute()
            logging.info(f"webhook response {resp}")
            while y:
                y = await check_patreon.patreon_check(p_date_converted, chapter)
                await asyncio.sleep(10)
        else:
            await asyncio.sleep(10)
    await get_patreon.get_last_patreon(conn)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
