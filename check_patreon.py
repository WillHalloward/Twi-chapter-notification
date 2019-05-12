import json
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
    for br in soup.find_all("br"):
        br.replace_with("\n")
    link_url = soup.find("a").text
    if title == chapter:
        textfile = open("chapter.txt", "w")
        print(title + "\n" + soup.text)
        clipboard.copy(title + "\n" + soup.text)
        textfile.write(link_url)
        return False
    return True
