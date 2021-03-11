import os

import psycopg2
from dotenv import load_dotenv
import urllib.parse as urlparse

load_dotenv()

def get_connection():
    """
    This function is used to form connection with the database based
    upon the fact if it is a local environment or dev environment.
    """

    if os.getenv('ENVIRONMENT') == 'local':
        conn = psycopg2.connect(
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port= os.getenv('DATABASE_PORT')
        )
    elif os.getenv('ENVIRONMENT') == 'dev':
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port


        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    conn.autocommit = True
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    return cursor
