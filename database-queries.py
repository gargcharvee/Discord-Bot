import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()
#establishing the connection
conn = psycopg2.connect(
    database=os.getenv('DATABASE'),
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port= os.getenv('DATABASE_PORT')
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = '''CREATE database "discord-bot-db"''';

#Creating a database
cursor.execute(sql)
print("Database created successfully........")

#Closing the connection
conn.close()

conn = psycopg2.connect(
    database=os.getenv('DATABASE_NAME'),
    user=os.getenv('DATABASE_USER'),
    password=os.getenv('DATABASE_PASSWORD'),
    host=os.getenv('DATABASE_HOST'),
    port= os.getenv('DATABASE_PORT')
)
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
conn.autocommit = True

#Creating table as per requirement
sql ='''CREATE TABLE member(
    id SERIAL PRIMARY KEY,
    channel_id VARCHAR(600) NOT NULL,
    user_id VARCHAR(600) NOT NULL,
    UNIQUE (channel_id, user_id)
)'''
cursor.execute(sql)
print("member created successfully........",)

sql ='''CREATE TABLE searches(
    id SERIAL PRIMARY KEY,
    search_text VARCHAR(600)
)'''
cursor.execute(sql)
print("searches created successfully........")

sql = '''CREATE TABLE search_history (
   member_id INTEGER NOT NULL,
   search_id INTEGER NOT NULL,
   PRIMARY KEY (member_id, search_id),
   FOREIGN KEY(member_id) REFERENCES member (id),
   FOREIGN KEY(search_id) REFERENCES searches (id)
)
'''
cursor.execute(sql)
print("searche history created successfully........")

#Closing the connection
conn.close()