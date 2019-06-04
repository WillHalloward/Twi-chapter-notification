# Patreon and website scraper & alerter

A program made to scrape and watch a website for changes and then alert by posting to discord and reddit when changes are detected. 

## Function

The script works by continusally watching a given url for a specfic element via beautfulsoup 4 and alerting if the elements changes. 

This trigger the second script which is either a reddit command to post the url to a subreddit, or to start watching a patreon page instead. 

If a post is detected on patreon which matches the condidtion given it will then post the content off the post to discord via a webhook. 

## Usage

To use for own use you need to create a "secrets.py" file which contains a couple of things depending on which part of the program you need. 

```python
# Patreon cookie
cookies = {'session_id': 'COOKIE HERE'}
# Discord webhooks
spidey_bot = "DISCORD WEBHOOK HERE"
# Reddit bot information
client_id = "client id here"
client_secret = "client secret here"
user_agent = "user agent here"
username = "username here"
password = "password here"

```

