import os

import praw

import secrets


def post_to_reddit(p_title):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    url = open(dir_path + "/chapter.txt", "r").read()
    reddit = praw.Reddit(client_id=secrets.client_id,
                         client_secret=secrets.client_secret,
                         user_agent=secrets.user_agent,
                         username=secrets.username,
                         password=secrets.password)

    wanderingInn = reddit.subreddit("WanderingInn")
    title = "[Discussion] - " + p_title
    wanderingInn.submit(title, url=url, flair_id="b8f4045a-f091-11e8-871f-0e4511bea43e")
