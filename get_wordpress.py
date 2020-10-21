import logging
import re
from datetime import datetime

from bs4 import BeautifulSoup


async def get_wordpress(page, conn):
    soup = BeautifulSoup(page.text, 'lxml')
    content_all = page.text
    title = soup.find("h1", {"class": "entry-title"}).text.strip()
    logging.info(f"Title {title}")
    body = soup.find("div", {"class": "entry-content"})
    for a in body.find_all('a', href=True):
        a.clear()
    content_post = body
    content_post_clean = body.text
    date = datetime.fromisoformat(soup.find("meta", {"property": "article:published_time"})['content'])
    logging.info(f"date: {date}")
    word_count = len(re.split(r'\S+', content_post_clean.strip()))
    logging.info(f"Wordcount {word_count}")
    invis_text = soup.find_all("span", {"style": "color:#0c0e0e;"})
    logging.info(f"invis text {invis_text}")
    page_id = soup.find("article")['id']
    logging.info(f"Page id: {page_id}")
    if invis_text:
        for tests in invis_text:
            text = tests.parent.text.replace(tests.text, f"**{tests.text}**").strip()
            await conn.execute("INSERT INTO invisible_text_twi(content, chapter_id, title, date) VALUES($1,$2,$3,$4)",
                               text, page_id, title, date)

    try:
        await conn.execute(
            "INSERT INTO wandering_inn(title, content_post_clean, content_post, content_all, date, link, word_count, id)"
            "VALUES ($1,$2,$3,$4,$5,$6,$7,$8)",
            title, content_post_clean.strip(), str(content_post), content_all, date, page.url, word_count, page_id)
    except Exception as e:
        logging.critical(f"Failed to insert into database {e}")

    await conn.close()
