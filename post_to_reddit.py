import logging

import praw

import secrets


def post_to_reddit(p_title, url):
    reddit = praw.Reddit(client_id=secrets.client_id,
                         client_secret=secrets.client_secret,
                         user_agent=secrets.user_agent,
                         username=secrets.username,
                         password=secrets.password)

    wanderingInn = reddit.subreddit("WanderingInn")
    title = "[Discussion] - " + p_title
    logging.info(f"Posting to subreddit {wanderingInn} with title {title} and url {url}")
    wanderingInn.submit(title, url=url)
