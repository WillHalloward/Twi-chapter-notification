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
    post = wanderingInn.submit(title, url=url, flair_id="b8f4045a-f091-11e8-871f-0e4511bea43e")
    post.reply(
        """Hey folks.

A reminder on the Patreon spoiler rules. **EVERYTHING** that's a part of the Patreon chapter
is considered a spoiler that isn't public information.

Also if you see what you think is a spoiler please use the report function and a mod will take a look at it.

Thanks!

Ps! Remember to vote for twi at http://topwebfiction.com/vote.php?for=the-wandering-inn""")
