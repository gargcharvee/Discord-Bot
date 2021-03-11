import os

import json
import discord
import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()

google_api_call_headers = {
    "x-rapidapi-key": os.getenv('X_RAPIDAPI_KEY'),
    "x-rapidapi-host": os.getenv('X_RAPIDAPI_HOST'),
    "useQueryString": "true"
}

def send_top_5_search_links(value_to_be_searched):

    response = requests.get(
        "https://google-search3.p.rapidapi.com/api/v1/search/q={}&num=5".format(
            '+'.join(value_to_be_searched.split(' '))
        ), headers=google_api_call_headers
    )
    json_response = {}
    if response.status_code == 200 and response.text:
        json_response = json.loads(response.text)

    list_of_links = []

    for result in json_response.get('results'):
        list_of_links.append(result['link'])

    return list_of_links

def add_search_results_in_db(cursor, text_searched, author_id, channel_id):
    # check if member object exists in db then get its id else create a new member object
    create_member_obj_sql = '''
        insert into member (channel_id, user_id)
        values({channel_id}, {user_id})
        on conflict (channel_id, user_id) do nothing
    '''.format(
        channel_id=channel_id, user_id=author_id
    )
    cursor.execute(create_member_obj_sql)

    get_memeber_obj_sql = '''
        select id from member where channel_id='{channel_id}' and user_id='{user_id}'
    '''.format(channel_id=channel_id, user_id=author_id)
    cursor.execute(get_memeber_obj_sql)
    (member_obj_id, ) = cursor.fetchone()

    # create search entry
    create_search_obj_sql = '''
        insert into searches (search_text) values('{text_searched}') returning id
    '''.format(text_searched=text_searched)
    cursor.execute(create_search_obj_sql)
    (search_obj_id, ) = cursor.fetchone()

    # add entry for search history
    create_search_history_obj = '''
        insert into search_history (member_id, search_id) values ('{member_obj_id}','{search_obj_id}')
    '''.format(
        member_obj_id=member_obj_id, search_obj_id=search_obj_id
    )
    cursor.execute(create_search_history_obj)


def google_search_functionality(cursor, text_searched, author_id, channel_id):
    """
    This function returns the top 5 links for the text searched and make the entry for
    the same in database.
    """
    links = send_top_5_search_links(text_searched)
    add_search_results_in_db(cursor, text_searched, author_id, channel_id)

    return links