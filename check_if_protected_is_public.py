import time

import clipboard
import requests
from ahk import AHK
from ahk.window import Window
from bs4 import BeautifulSoup

x = True
# url = "https://wanderinginn.com/2019/05/07/6-14-k/"
file = open("chapter.txt", "r")
url = file.read()
ahk = AHK()
while x:
    startPage = requests.get(url)
    soup = BeautifulSoup(startPage.content, "lxml")
    post = soup.find("header", {"class": "entry-header"})
    post_text = post.text.partition(' ')[0]
    if post_text == "\nProtected:":
        print("Chapter is Protected")
        time.sleep(2)
    else:
        print("Chapter is public")
        print(url)
        win = Window.from_pid(ahk, pid='12608')
        clipboard.copy(url)
        win.activate()
        time.sleep(0.1)
        ahk.send_input("^t")
        time.sleep(0.2)
        ahk.send_input("public-spoilers")
        time.sleep(0.2)
        ahk.send_input("{enter}")
        time.sleep(0.2)
        ahk.send_input("{Esc}{Esc}")
        time.sleep(0.2)
        ahk.send_input("^v Chapter public{enter}")
        x = False
