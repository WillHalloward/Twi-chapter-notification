import re
from datetime import datetime

import asyncpg as asyncpg
from bs4 import BeautifulSoup


async def get_all_wordpress(page, conn):
    check_dupe = await conn.fetchrow("SELECT exists(select 1 from wandering_inn where table_of_content_link=$1)",
                                     page.url)
    if check_dupe['exists']:
        print(f"{page.url} Exists in database")
        return
    soup = BeautifulSoup(page.text, 'lxml')
    content_all = page.text
    title = soup.find("h1", {"class": "entry-title"}).text.strip()
    body = soup.find("div", {"class": "entry-content"})
    for a in body.find_all('a', href=True):
        a.clear()
    content_post = body
    content_post_clean = body.text
    date = datetime.fromisoformat(soup.find("meta", {"property": "article:published_time"})['content'])
    word_count = len(re.split(r'\S+', content_post_clean.strip()))
    try:
        await conn.execute(
            "INSERT INTO wandering_inn(title, content_post_clean, content_post, content_all, date, link, word_count) "
            "VALUES ($1,$2,$3,$4,$5,$6,$7)",
            title, content_post_clean.strip(), str(content_post), content_all, date, page.url, word_count)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    await conn.close()
