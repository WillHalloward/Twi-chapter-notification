import json
from datetime import datetime

import aiohttp
import asyncpg

import secrets


async def fetch(session, url):
    async with session.get(url, cookies=secrets.cookies) as response:
        return await response.text()


async def get_all_patreon(conn):
    link = "https://www.patreon.com/api/posts?include=user%2Cattachments%2Cuser_defined_tags%2Ccampaign%2Cpoll.choices%2Cpoll.current_user_responses.user%2Cpoll.current_user_responses.choice%2Cpoll.current_user_responses.poll%2Caccess_rules.tier.null%2Cimages.null%2Caudio.null&fields[post]=change_visibility_at%2Ccomment_count%2Ccontent%2Ccurrent_user_can_delete%2Ccurrent_user_can_view%2Ccurrent_user_has_liked%2Cembed%2Cimage%2Cis_paid%2Clike_count%2Cmin_cents_pledged_to_view%2Cpost_file%2Cpost_metadata%2Cpublished_at%2Cpatron_count%2Cpatreon_url%2Cpost_type%2Cpledge_url%2Cthumbnail_url%2Cteaser_text%2Ctitle%2Cupgrade_url%2Curl%2Cwas_posted_by_campaign_owner&fields[user]=image_url%2Cfull_name%2Curl&fields[campaign]=show_audio_post_download_links%2Cavatar_photo_url%2Cearnings_visibility%2Cis_nsfw%2Cis_monthly%2Cname%2Curl&fields[access_rule]=access_rule_type%2Camount_cents&fields[media]=id%2Cimage_urls%2Cdownload_url%2Cmetadata%2Cfile_name&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true&json-api-use-default-includes=false&json-api-version=1.0"
    await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
    while True:
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, link)
            json_data = json.loads(html)
        for posts in json_data['data']:
            comment_count = posts['attributes']['comment_count']
            try:
                content = posts['attributes']['content']
            except KeyError:
                content = None
            like_count = posts['attributes']['like_count']
            min_cents_pledged_to_view = posts['attributes']['min_cents_pledged_to_view']
            post_type = posts['attributes']['post_type']
            published_at = datetime.fromisoformat(posts['attributes']['published_at'])
            title = posts['attributes']['title']
            print(title)
            url = posts['attributes']['url']
            post_id = posts['id']
            try:
                image = posts['attributes']['image']['large_url']
            except TypeError:
                image = None
            try:
                await conn.execute(
                    "INSERT INTO "
                    "patreon_twi(post_id, title, content, comment_count, like_count, url, min_cents_pledged_to_view, post_type, published_at, image, body) "
                    "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::json)",
                    int(post_id), title, content, comment_count, like_count, url, min_cents_pledged_to_view,
                    post_type, published_at, image, posts)
            except asyncpg.exceptions.UniqueViolationError:
                pass
        try:
            link = json_data['links']['next']
        except KeyError:
            break
    await conn.execute("UPDATE patreon_twi "
                       "SET password=subquery.pass "
                       "FROM "
                       "(SELECT SUBSTRING(content, '<p><br></p><p>(.?(''?\w[\w'']*(?:-\w+)*.{0,3})|.*: (''?\w[\w'']*(?:-\w+)*''?\??\.*))</p>') as pass, serial_id "
                       "FROM patreon_twi "
                       "WHERE post_type = 'text_only' "
                       "AND lower(title) not similar to lower('%Side Stor%') "
                       "AND serial_id NOT IN (1,3,6,7,8,10,15,18,34,97,134,185,189,243,269,116)) "
                       "AS subquery "
                       "WHERE patreon_twi.serial_id=subquery.serial_id AND patreon_twi.password IS NOT NULL;")


async def get_last_patreon(conn):
    link = "https://www.patreon.com/api/posts?include=user%2Cattachments%2Cuser_defined_tags%2Ccampaign%2Cpoll.choices%2Cpoll.current_user_responses.user%2Cpoll.current_user_responses.choice%2Cpoll.current_user_responses.poll%2Caccess_rules.tier.null%2Cimages.null%2Caudio.null&fields[post]=change_visibility_at%2Ccomment_count%2Ccontent%2Ccurrent_user_can_delete%2Ccurrent_user_can_view%2Ccurrent_user_has_liked%2Cembed%2Cimage%2Cis_paid%2Clike_count%2Cmin_cents_pledged_to_view%2Cpost_file%2Cpost_metadata%2Cpublished_at%2Cpatron_count%2Cpatreon_url%2Cpost_type%2Cpledge_url%2Cthumbnail_url%2Cteaser_text%2Ctitle%2Cupgrade_url%2Curl%2Cwas_posted_by_campaign_owner&fields[user]=image_url%2Cfull_name%2Curl&fields[campaign]=currency%2Cshow_audio_post_download_links%2Cavatar_photo_url%2Cearnings_visibility%2Cis_nsfw%2Cis_monthly%2Cname%2Curl&fields[access_rule]=access_rule_type%2Camount_cents&fields[media]=id%2Cimage_urls%2Cdownload_url%2Cmetadata%2Cfile_name&sort=-published_at&filter[campaign_id]=568211&filter[is_draft]=false&filter[contains_exclusive_posts]=true&json-api-use-default-includes=false&json-api-version=1.0"
    await conn.set_type_codec('json', encoder=json.dumps, decoder=json.loads, schema='pg_catalog')
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, link)
        json_data = json.loads(html)
    for posts in reversed(json_data['data']):
        comment_count = posts['attributes']['comment_count']
        try:
            content = posts['attributes']['content']
        except KeyError:
            content = None
        like_count = posts['attributes']['like_count']
        min_cents_pledged_to_view = posts['attributes']['min_cents_pledged_to_view']
        post_type = posts['attributes']['post_type']
        published_at = datetime.fromisoformat(posts['attributes']['published_at'])
        title = posts['attributes']['title']
        print(title)
        url = posts['attributes']['url']
        post_id = posts['id']
        try:
            image = posts['attributes']['image']['large_url']
        except TypeError:
            image = None
        try:
            await conn.execute(
                "INSERT INTO "
                "patreon_twi(post_id, title, content, comment_count, like_count, url, min_cents_pledged_to_view, post_type, published_at, image, body) "
                "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::json)",
                int(post_id), title, content, comment_count, like_count, url, min_cents_pledged_to_view,
                post_type, published_at, image, posts)
        except asyncpg.exceptions.UniqueViolationError:
            pass
    await conn.execute("UPDATE patreon_twi "
                       "SET password=subquery.pass "
                       "FROM "
                       "(SELECT SUBSTRING(content, '<p><br></p><p>(.?(''?\w[\w'']*(?:-\w+)*.{0,3})|.*: (''?\w[\w'']*(?:-\w+)*''?\??\.*))</p>') as pass, serial_id "
                       "FROM patreon_twi "
                       "WHERE post_type = 'text_only' "
                       "AND lower(title) not similar to lower('%Side Stor%') "
                       "AND serial_id NOT IN (1,3,6,7,8,10,15,18,34,97,134,185,189,243,269,116)) "
                       "AS subquery "
                       "WHERE patreon_twi.serial_id=subquery.serial_id AND patreon_twi.password IS NOT NULL;")
