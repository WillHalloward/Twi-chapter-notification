import json
import re

import clipboard
import requests
from bs4 import BeautifulSoup


def patreon_check(chapter):
    cookies = {'session_id': 'X1Cxh3UoEqxjjf13pLcWwowFcJIta5EEbjrQK-SZRL4'}
    page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true",
        cookies=cookies)
    json_data = json.loads(page.text)
    body = json_data['data'][0]['attributes']['content']
    title = json_data['data'][0]['attributes']['title']
    soup = BeautifulSoup(body, "lxml")

    word_count = re.search("\((.*?)\)", body).group()
    password = re.search("(?<=<br></p><p>)(.*)(?=</p><p><br>)", body).group()
    link_url = soup.find("a").text
    if title == chapter:
        print(title)
        print(word_count)
        print(link_url)
        print(password)
        clipboard.copy(title + "\n" + word_count + "\n" + link_url + "\n" + password)
        return False
    return True
