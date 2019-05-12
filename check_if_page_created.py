import time
from datetime import datetime
import clipboard
import requests
from ahk import AHK
from bs4 import BeautifulSoup

import check_patreon

today_date = datetime.today().strftime('%Y/%m/%d')
ahk = AHK()
x = True
url = "https://wanderinginn.com/" + today_date
# url = "https://wanderinginn.com/2019/05/11/6-15-k/"
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("h1", {"class": "entry-title"})
    if post.text != "This is somewhat embarrassing, isn’t it?":
        post_text = post.text.split(' ')[0]
        chapter = post.text.split(':')[1]
        chapter = chapter.strip()
        print(chapter)
        if post_text == "Protected:":
            print("Chapter is posted")
            x = False
            y = True
            clipboard.copy(url)
            ahk.run_script("WinActivate, ahk_exe discord.exe", blocking=False)
            time.sleep(0.1)
            ahk.send_input("^t")
            time.sleep(0.2)
            ahk.send_input("patreon-spoilers")
            time.sleep(0.2)
            ahk.send_input("{enter}")
            time.sleep(0.2)
            ahk.send_input("{Esc}{Esc}")
            time.sleep(0.2)
            ahk.send_input("^v")
            time.sleep(0.2)
            #ahk.send_input("{enter}")
            while y:
                y = check_patreon.patreon_check(chapter)
            ahk.run_script("WinActivate, ahk_exe discord.exe", blocking=False)
            time.sleep(0.1)
            ahk.send_input("^t")
            time.sleep(0.2)
            ahk.send_input("patreon-spoilers")
            time.sleep(0.2)
            ahk.send_input("{enter}")
            time.sleep(0.2)
            ahk.send_input("{Esc}{Esc}")
            time.sleep(0.2)
            ahk.send_input("^v")
            time.sleep(0.2)
            #ahk.send_input("{enter}")

    else:
        print("Chapter is not created")
        time.sleep(2)
