import os

import json
import discord
import psycopg2
import requests
from dotenv import load_dotenv
import urllib.parse as urlparse

from bot_functions.google_search_function import google_search_functionality
from bot_functions.get_recent_searches_function import get_list_of_recent_searches

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

print (url, dbname, user, password, host, port)

conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
#establishing the connection
# conn = psycopg2.connect(
#    database=os.getenv('DATABASE_NAME'),
#    user=os.getenv('DATABASE_USER'),
#    password=os.getenv('DATABASE_PASSWORD'),
#    host=os.getenv('DATABASE_HOST'),
#    port= os.getenv('DATABASE_PORT')
# )
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Case 1: Bot replies hey if you type Hi
    if message.content.lower() == 'hi':
        await message.channel.send("hey")
    
    # Case 2: Bot replies with the top 5 links from the google if you search something
    # after writing !google like !google search
    if message.content.startswith('!google'):
        text_searched = message.content.split("!google",1)[1]
        # links = send_top_5_search_links(text_searched)
        # add_search_results_in_db(text_searched, message.author.id, message.channel.id)
        links = google_search_functionality(cursor, text_searched, message.author.id, message.channel.id)
        message_to_be_sent = '\n'.join(links) if links else 'Could not find any link. Please try again after some time.'
        await message.channel.send(message_to_be_sent)
    
    # Case 3: Bot checks you recent searched items if you type something after !recent.
    # like !recent search (It returns the searched which inlcudes those keywords)
    if message.content.startswith('!recent'):
        result = get_list_of_recent_searches(
            cursor,
            message.content.split("!recent",1)[1],
            message.author.id,
            message.channel.id
        )
        message_to_be_sent = '\n'.join([row[0] for row in result]) if result else 'No recent searches found'
        await message.channel.send(message_to_be_sent)

client.run(TOKEN)

#Closing the connection
conn.close()