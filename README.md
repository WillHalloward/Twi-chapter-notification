# patreon-scraping-twi
A python script to automaticly alert and post when a new chapter from The wandering inn is posted or made public. 
Works via the request library, Beautiful soup 4 and patreon api. 

Check_if_page_created.py needs a valid www.patreon.com cookie with subcription to https://www.patreon.com/pirateaba/posts for validation to reach the patreon post content. 
The patreon target can be changed via changing "[campaign_id]=xxxxxxxx"
  page = requests.get(
        "https://www.patreon.com/api/posts?sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true"
in check_patreon.py
