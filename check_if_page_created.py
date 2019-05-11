import os
import time
from datetime import datetime
import clipboard
import requests
from ahk import AHK
from ahk.window import Window
from bs4 import BeautifulSoup

import check_patreon
today_date = datetime.today().strftime('%Y/%m/%d')
ahk = AHK(executable_path = "C:\\Program Files\\AutoHotkey\\AutoHotkey.exe")
pid = os.getppid()
x = True
url = "https://wanderinginn.com/2019/05/11/6-15/"
while x:
    startPage = requests.get(url)
    #startPage = requests.get("https://wanderinginn.com/2019/05/07/6-14/")
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("h1", {"class" : "entry-title"})
    if post.text != "This is somewhat embarrassing, isn’t it?":
        post_text = post.text.split(' ')[0]
        chapter = post.text.split(':')[1]
        chapter = chapter.strip()
        print(chapter)
        if post_text == "Protected:":
            print("Chapter is posted")
            x = False
            y = True
            win = Window.from_pid(ahk, pid='10560')
            clipboard.copy(url)
            win.activate()
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
            ahk.send_input("{enter}")
            while y:
                y = check_patreon.patreon_check(chapter)
            win.activate()
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
            ahk.send_input("{enter}")

    else:
        print("Chapter is not created")
        time.sleep(1)