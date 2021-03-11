# Discord Bot

This is a discord bot which provides the following functionalities-

- It replies hey to your hi.

- A user can search on google through discord. If the user types !google nodejs, reply with top 5 links that you would get when you search nodejs on google.com

- Can search through your search history. If a user uses !google to search for "nodejs" "apple games" "game of thrones", and after these searches, if user types !recent game, your bot should reply with "apple games" and "game of thrones"

- The user search history is persistent. It used postgres database to store the recent searches done by a particular user in particular database.

## Installation

- Make a new virtual environment using python 3.7.9 version.

- Install the requirements from requirements.txt file.

- Install postgres.

## Setup

- To make database changes run the following command
```bash
python database-queries.py
```

- Make a .env file from .env.template file

- Run the following command to start your bot
```bash
python bot.py
```
