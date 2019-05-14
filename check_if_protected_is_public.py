import time

import clipboard
import requests
from ahk import AHK
from bs4 import BeautifulSoup
from datetime import datetime

x = True
# url = "https://wanderinginn.com/2019/05/07/6-14-k/"
url = open("chapter.txt", "r").read()
ahk = AHK()
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("header", {"class": "entry-header"})
    post_text = post.text.partition(' ')[0]
    if post_text == "\nProtected:":
        time_now = datetime.today().strftime('%X')
        print("[" + time_now + "] Chapter is Protected")
        time.sleep(10)
    else:
        print("Chapter is public")
        print(url)
        clipboard.copy(url + " Chapter public")
        ahk.run_script("WinActivate, ahk_exe discord.exe", blocking=False)
        time.sleep(0.2)
        win = ahk.active_window
        ahk.send_input("^t")
        time.sleep(0.2)
        ahk.send_input("public-spoilers")
        time.sleep(0.2)
        ahk.send_input("{enter}")
        time.sleep(0.2)
        ahk.send_input("{Esc}{Esc}")
        time.sleep(0.2)
        if win.title == b"#public-spoilers - Discord":
            ahk.send_input("^a^v")
            time.sleep(0.2)
            ahk.send_input("{enter}")
        else:
            print("Error, channel not found/Discord not open")
            exit()
        x = False
