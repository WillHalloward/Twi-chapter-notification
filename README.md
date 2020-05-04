# Wandering inn chapter notifier

A script made to repededly refresh wanderinginn.com for changes and then notify the wandering inn discord server. 

## Function

The script works by continually watching a given URL for a specific element via beautifulsoup 4 and alerting if the elements changes. 

This trigger the second script which is either a reddit command to post the URL to a subreddit, or to start watching a patreon page instead. 

If a post is detected on patreon which matches the condition given it will then post the content off the post to discord via a webhook. 
